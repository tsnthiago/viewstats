from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import numpy as np
from app.services.topic_generator import TopicGenerator
from app.services.embedding_service import get_openai_embeddings
import asyncio

class QdrantService:
    def __init__(self, host: str = 'qdrant', port: int = 6333, collection_name: str = 'videos_viewstats'):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            if self.collection_name not in [c.name for c in self.client.get_collections().collections]:
                self.client.recreate_collection(
                    collection_name=self.collection_name,
                    vectors_config={"size": 1536, "distance": "Cosine"}  # 1536 para text-embedding-3-small
                )
        except Exception:
            pass

    def insert_vector(self, id: int, vector: list[float], payload: dict = None):
        point = PointStruct(id=id, vector=vector, payload=payload or {})
        self.client.upsert(collection_name=self.collection_name, points=[point])
        return {"status": "ok", "id": id}

    def index_video_with_topics(self, id: int, vector: list[float], title: str, description: str, transcript: str, channel_id: str = None):
        """
        Pipeline: gera tópicos com LLM, monta payload e insere no Qdrant.
        """
        # TODO: Chamar TopicGenerator e montar payload
        raise NotImplementedError("Pipeline de indexação com tópicos não implementado.")

    async def search_vectors(self, query: str = None, topic_filter: str = None, top_k: int = 10):
        """
        Busca real: se query, faz busca vetorial; se não, faz scroll. Sempre aplica filtro por tópico se fornecido.
        """
        filter_ = None
        if topic_filter:
            filter_ = {
                "must": [
                    {"key": "taxonomy_ids", "match": {"value": topic_filter}}
                ]
            }
        if query and query.strip():
            # Busca vetorial real com OpenAI
            query_vec = (await get_openai_embeddings([query]))[0]
            hits = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vec,
                limit=top_k,
                query_filter=filter_
            )
            results = []
            for point in hits:
                payload = point.payload or {}
                results.append({
                    "id": payload.get("yt_id", str(point.id)),
                    "score": point.score,
                    "title": payload.get("title", ""),
                    "description": payload.get("description_llm", ""),
                    "topics_path": payload.get("taxonomy_ids", [])
                })
            return results
        else:
            # Scroll (sem query)
            hits = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=filter_,
                limit=top_k
            )[0]
            results = []
            for point in hits:
                payload = point.payload or {}
                results.append({
                    "id": payload.get("yt_id", str(point.id)),
                    "score": 1.0,
                    "title": payload.get("title", ""),
                    "description": payload.get("description_llm", ""),
                    "topics_path": payload.get("taxonomy_ids", [])
                })
            return results 