from fastapi import APIRouter
from app.models.search import SearchRequest
from typing import List
from pydantic import BaseModel, Field
from fastapi import Body

router = APIRouter()

class SearchResultItem(BaseModel):
    id: str = Field(..., example="video1")
    score: float = Field(..., example=0.92)
    title: str = Field(..., example="Como usar FastAPI")
    description: str = Field(..., example="Tutorial completo de FastAPI para APIs modernas.")
    topics_path: List[str] = Field(..., example=["Tecnologia > Programação > Python"])

class SearchResponse(BaseModel):
    results: List[SearchResultItem]

@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Busca semântica de vídeos",
    response_description="Lista de vídeos relevantes",
    tags=["Busca"],
    description="""
    Realiza busca semântica por vídeos, podendo filtrar por tópico hierárquico.
    Retorna os vídeos mais relevantes de acordo com o embedding e o filtro.
    """,
    responses={
        200: {
            "description": "Busca realizada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "results": [
                            {
                                "id": "video1",
                                "score": 0.92,
                                "title": "Como usar FastAPI",
                                "description": "Tutorial completo de FastAPI para APIs modernas.",
                                "topics_path": ["Tecnologia > Programação > Python"]
                            }
                        ]
                    }
                }
            }
        }
    }
)
def search(
    request: SearchRequest = Body(
        ..., 
        example={
            "query": "FastAPI",
            "topic_filter": "Tecnologia > Programação > Python",
            "top_k": 5
        }
    )
):
    """Busca semântica de vídeos com filtro opcional de tópico."""
    # Simular embedding e busca no Qdrant
    # No futuro: gerar embedding real e consultar Qdrant
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
    return SearchResponse(results=dummy_results[:request.top_k]) 