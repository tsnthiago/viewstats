from fastapi import APIRouter, Query, Body, Request
from app.models.search import SearchRequest
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from app.services.qdrant_service import QdrantService
import os

router = APIRouter()

class SearchResultItem(BaseModel):
    id: str = Field(..., example="video1")
    score: float = Field(..., example=0.92)
    title: str = Field(..., example="Como usar FastAPI")
    description: str = Field(..., example="Tutorial completo de FastAPI para APIs modernas.")
    topics_path: List[str] = Field(..., example=["Tecnologia > Programação > Python"])

class SearchResponse(BaseModel):
    results: List[SearchResultItem]
    total: int

qdrant_service = QdrantService(
    host="qdrant",
    port=6333,
    collection_name=os.environ.get("QDRANT_COLLECTION_NAME", "videos_viewstats")
)

@router.get("/search", response_model=SearchResponse)
def search_get(
    q: Optional[str] = Query("", alias="q"),
    topic_filter: Optional[str] = Query(None),
    page: int = Query(1),
    limit: int = Query(12)
):
    """GET /search para compatibilidade temporária com frontend (dados mockados)."""
    dummy_results = [
        SearchResultItem(
            id="video1",
            score=0.92,
            title="Como usar FastAPI",
            description="Tutorial completo de FastAPI para APIs modernas.",
            topics_path=["Tecnologia > Programação > Python"]
        ),
        SearchResultItem(
            id="video2",
            score=0.89,
            title="Introdução ao Qdrant",
            description="Como usar Qdrant para busca vetorial.",
            topics_path=["Tecnologia > IA > Busca Semântica"]
        )
    ]
    return SearchResponse(results=dummy_results[:limit], total=2)

@router.post("/search", response_model=SearchResponse)
async def search_post(request: SearchRequest = Body(...)):
    """POST /search (agora busca real no Qdrant, assíncrono)."""
    results = await qdrant_service.search_vectors(
        query=request.query,
        topic_filter=request.topic_filter,
        top_k=request.top_k
    )
    return SearchResponse(results=results, total=len(results)) 