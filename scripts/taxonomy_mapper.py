import json
import os
from typing import Dict, List, Any

CANONICAL_TAXONOMY_PATH = os.path.join('data', 'canonical_taxonomy.json')
PROCESSED_VIDEOS_PATH = os.path.join('data', 'processed_videos.json')
OUTPUT_MAP_PATH = os.path.join('data', 'video_to_taxonomy_map.json')

# --- Etapa 1: Atribuir IDs únicos à taxonomia canônica ---
def add_ids_to_taxonomy(taxonomy: Dict[str, Any], path: List[str] = None) -> Dict[str, Any]:
    if path is None:
        path = []
    taxonomy_with_ids = {}
    for key, value in taxonomy.items():
        current_path = path + [key]
        node_id = '-'.join([p.lower().replace(' ', '_') for p in current_path])
        if isinstance(value, dict) and value:
            taxonomy_with_ids[key] = add_ids_to_taxonomy(value, current_path)
            taxonomy_with_ids[key]['__id__'] = node_id
        else:
            taxonomy_with_ids[key] = {'__id__': node_id}
    return taxonomy_with_ids

# --- Etapa 2: Criar mapa de caminho para ID ---
def build_path_to_id_map(taxonomy: Dict[str, Any], path: List[str] = None, result: Dict[str, str] = None) -> Dict[str, str]:
    if path is None:
        path = []
    if result is None:
        result = {}
    for key, value in taxonomy.items():
        if not isinstance(value, dict):
            continue
        current_path = path + [key]
        path_str = ' > '.join(current_path)
        node_id = value.get('__id__')
        if node_id:
            result[path_str.lower()] = node_id
        # Recursão para filhos
        for subkey, subval in value.items():
            if subkey != '__id__' and isinstance(subval, dict):
                build_path_to_id_map({subkey: subval}, current_path, result)
    return result

# --- Etapa 3: Mapear vídeos para IDs da taxonomia ---
def map_videos_to_taxonomy(processed_videos: List[Dict[str, Any]], path_to_id: Dict[str, str], checkpoint_path=OUTPUT_MAP_PATH) -> Dict[str, List[str]]:
    # Checkpoint: carregar progresso parcial
    video_map = {}
    if os.path.exists(checkpoint_path):
        try:
            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                video_map = json.load(f)
            print(f"[MAPPER] Checkpoint: {len(video_map)} vídeos já mapeados serão pulados.")
        except Exception as e:
            print(f"[MAPPER] Falha ao ler checkpoint, começando do zero. Erro: {e}")
            video_map = {}
    for video in processed_videos:
        yt_id = video.get('yt_id')
        if yt_id in video_map:
            continue  # Pular vídeos já mapeados
        topics = video.get('hierarchical_topics', [])
        ids = []
        for topic_path in topics:
            topic_path_norm = topic_path.strip().lower()
            node_id = path_to_id.get(topic_path_norm)
            if node_id:
                ids.append(node_id)
        if ids:
            video_map[yt_id] = ids
            # Salvar progresso incremental
            with open(checkpoint_path, 'w', encoding='utf-8') as f:
                json.dump(video_map, f, indent=2, ensure_ascii=False)
    return video_map

if __name__ == '__main__':
    # Carregar taxonomia canônica
    with open(CANONICAL_TAXONOMY_PATH, 'r', encoding='utf-8') as f:
        canonical_taxonomy = json.load(f)
    # Adicionar IDs
    taxonomy_with_ids = add_ids_to_taxonomy(canonical_taxonomy)
    # Construir mapa de caminho para ID
    path_to_id = build_path_to_id_map(taxonomy_with_ids)
    # Carregar vídeos processados
    with open(PROCESSED_VIDEOS_PATH, 'r', encoding='utf-8') as f:
        processed_videos = json.load(f)
    # Mapear vídeos
    video_to_taxonomy_map = map_videos_to_taxonomy(processed_videos, path_to_id)
    # Salvar resultado
    with open(OUTPUT_MAP_PATH, 'w', encoding='utf-8') as f:
        json.dump(video_to_taxonomy_map, f, indent=2, ensure_ascii=False)
    print(f"Mapeamento salvo em {OUTPUT_MAP_PATH} ({len(video_to_taxonomy_map)} vídeos mapeados)") 