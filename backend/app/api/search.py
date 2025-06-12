from fastapi import APIRouter, Query, Body, Request
from app.models.search import SearchRequest
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

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
def search_post(request: SearchRequest = Body(...)):
    """POST /search (mantém lógica mockada)."""
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
    return SearchResponse(results=dummy_results[:request.top_k], total=2) 