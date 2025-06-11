from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import numpy as np

class QdrantService:
    def __init__(self, host: str = 'qdrant', port: int = 6333, collection_name: str = 'videos'):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self._ensure_collection()

    def _ensure_collection(self):
        if self.collection_name not in [c.name for c in self.client.get_collections().collections]:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config={"size": 384, "distance": "Cosine"}
            )

    def insert_vector(self, id: int, vector: list[float], payload: dict = None):
        point = PointStruct(id=id, vector=vector, payload=payload or {})
        self.client.upsert(collection_name=self.collection_name, points=[point])
        return {"status": "ok", "id": id} 