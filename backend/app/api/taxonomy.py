from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import os
import json

router = APIRouter()

MOCK_TAXONOMY = [
    {"id": "ai", "name": "Artificial Intelligence", "videoCount": 35},
    {"id": "ml", "name": "Machine Learning", "videoCount": 28},
    {"id": "web-dev", "name": "Web Development", "videoCount": 42},
    {"id": "react", "name": "React", "videoCount": 24},
    {"id": "python", "name": "Python", "videoCount": 31},
    {"id": "data-science", "name": "Data Science", "videoCount": 19},
]

@router.get(
    "/taxonomy",
    summary="Retorna a árvore de tópicos",
    response_description="Árvore de tópicos em formato JSON",
    tags=["Taxonomia"],
    description="""
    Retorna a árvore de tópicos hierárquica utilizada para navegação e filtragem no frontend.
    """,
    responses={
        200: {
            "description": "Taxonomia retornada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "taxonomy": [
                            {"name": "Tecnologia", "_children": [
                                {"name": "Programação", "_children": [
                                    {"name": "Python", "_children": []}
                                ]}
                            ]}
                        ]
                    }
                }
            }
        }
    }
)
def get_taxonomy(flat: bool = Query(False, description="Return flat array if true")):
    """Endpoint GET /taxonomy — retorna a árvore de tópicos do taxonomy.json ou mock."""
    if flat:
        return MOCK_TAXONOMY
    # Resposta padrão (mantém compatibilidade)
    return {"taxonomy": MOCK_TAXONOMY} 