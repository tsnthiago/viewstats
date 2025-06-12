import os
import json
import uuid
from typing import List, Dict, Any
import pandas as pd
from tqdm import tqdm
from config import Config
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from embedding_service import get_openai_embeddings
import asyncio

BATCH_SIZE = 64

# --- Utilitário para gerar UUID determinístico a partir do yt_id ---
def uuid_from_ytid(yt_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, yt_id))

# --- Garantir existência da coleção ---
def ensure_collection(client: QdrantClient, vector_size: int, collection_name: str):
    collections = client.get_collections().collections
    if not any(c.name == collection_name for c in collections):
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=qmodels.VectorParams(
                size=vector_size,
                distance=qmodels.Distance.COSINE
            )
        )
        print(f"Coleção '{collection_name}' criada.")
    else:
        print(f"Coleção '{collection_name}' já existe.")

# --- Carregar e preparar dados ---
def load_data():
    with open(os.path.join('data', 'processed_videos.json'), encoding='utf-8') as f:
        videos = json.load(f)
    with open(os.path.join('data', 'video_to_taxonomy_map.json'), encoding='utf-8') as f:
        video_to_tax = json.load(f)
    return videos, video_to_tax

# --- Preparar DataFrame unificado ---
def prepare_dataframe(videos: List[Dict[str, Any]], video_to_tax: Dict[str, List[str]]) -> pd.DataFrame:
    df = pd.DataFrame(videos)
    # Corrigir nomes de colunas essenciais se foram renomeadas por duplicidade
    required_cols = ['yt_id', 'title', 'description_llm', 'intention', 'named_entities', 'hierarchical_topics']
    for col in required_cols:
        if col not in df.columns:
            # Tentar encontrar uma coluna que começa com o nome base
            candidates = [c for c in df.columns if c.startswith(col)]
            if candidates:
                df = df.rename(columns={candidates[0]: col})
            else:
                raise ValueError(f"Coluna essencial '{col}' não encontrada no DataFrame para indexação.")
    df['taxonomy_ids'] = df['yt_id'].map(video_to_tax).apply(lambda x: x if isinstance(x, list) else [])
    # Extrair apenas nomes das entidades
    def extract_names(entities):
        if isinstance(entities, list):
            return [e['name'] for e in entities if isinstance(e, dict) and 'name' in e]
        return []
    df['named_entities'] = df['named_entities'].apply(extract_names)
    return df

# --- Gerar embeddings em lote ---
async def batch_embeddings_openai(texts: List[str], batch_size: int = 1000) -> List[List[float]]:
    return await get_openai_embeddings(texts)

# --- Indexar no Qdrant ---
async def index_to_qdrant_async(df: pd.DataFrame, client: QdrantClient, collection_name: str):
    # Garante que a coleção exista antes de indexar
    ensure_collection(client, vector_size=1536, collection_name=collection_name)  # 1536 para text-embedding-3-small
    checkpoint_path = os.path.join('data', 'indexed_ytids.json')
    indexed_ytids = set()
    if os.path.exists(checkpoint_path):
        try:
            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                indexed_ytids = set(json.load(f))
            print(f"[INDEXER] Checkpoint: {len(indexed_ytids)} vídeos já indexados encontrados.")
        except Exception as e:
            print(f"[INDEXER] Falha ao ler checkpoint, começando do zero. Erro: {e}")
            indexed_ytids = set()
    # Filtrar df para só indexar vídeos não indexados
    df_to_index = df[~df['yt_id'].isin(indexed_ytids)]
    print(f"[INDEXER] {len(df_to_index)} novos vídeos para indexar.")
    if len(df_to_index) == 0:
        print("[INDEXER] Nenhum vídeo novo para indexar. Processo concluído.")
        return
        
    texts = (df_to_index['title'].fillna('') + ' ' + df_to_index['description_llm'].fillna('')).tolist()
    
    print("[INDEXER] Gerando embeddings com OpenAI...")
    embeddings = await batch_embeddings_openai(texts)
    print(f"[INDEXER] {len(embeddings)} embeddings gerados.")

    assert len(embeddings) == len(df_to_index)
    ids = [uuid_from_ytid(ytid) for ytid in df_to_index['yt_id']]
    payloads = []
    for _, row in df_to_index.iterrows():
        payloads.append({
            'yt_id': row['yt_id'],
            'title': row['title'],
            'description_llm': row['description_llm'],
            'intention': row.get('intention', ''),
            'named_entities': row.get('named_entities', []),
            'taxonomy_ids': row.get('taxonomy_ids', [])
        })

    if payloads:
        print(f"[INDEXER] Exemplo de payload a ser enviado: {json.dumps(payloads[0], indent=2, ensure_ascii=False)}")

    # Indexar em lotes
    for i in tqdm(range(0, len(df_to_index), BATCH_SIZE), desc='Indexando lotes no Qdrant'):
        batch_ids = ids[i:i+BATCH_SIZE]
        batch_vectors = embeddings[i:i+BATCH_SIZE]
        batch_payloads = payloads[i:i+BATCH_SIZE]
        points = [
            qmodels.PointStruct(
                id=pid,
                vector=vec,
                payload=pld
            ) for pid, vec, pld in zip(batch_ids, batch_vectors, batch_payloads)
        ]
        try:
            response = client.upsert(collection_name=collection_name, points=points, wait=True)
            print(f"[INDEXER] Lote {i//BATCH_SIZE + 1} enviado. Status: {response.status}")
        except Exception as e:
            print(f"[INDEXER] Erro ao enviar lote para o Qdrant: {e}")
            continue

        # Salvar checkpoint incremental
        batch_ytids = list(df_to_index['yt_id'].iloc[i:i+BATCH_SIZE])
        indexed_ytids.update(batch_ytids)
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(list(indexed_ytids), f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    print('Carregando modelo de embeddings...')
    model = SentenceTransformer(Config.EMBEDDING_MODEL)
    print('Conectando ao Qdrant...')
    client = QdrantClient(url=Config.QDRANT_URL)
    ensure_collection(client, vector_size=384, collection_name=Config.QDRANT_COLLECTION_NAME)
    print('Carregando dados...')
    videos, video_to_tax = load_data()
    df = prepare_dataframe(videos, video_to_tax)
    print(f'{len(df)} vídeos prontos para indexação.')
    asyncio.run(index_to_qdrant_async(df, client, Config.QDRANT_COLLECTION_NAME))
    print('Indexação concluída.') 