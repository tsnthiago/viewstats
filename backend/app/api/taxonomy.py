from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os
import json

router = APIRouter()

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
def get_taxonomy():
    """Endpoint GET /taxonomy — retorna a árvore de tópicos do taxonomy.json."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "taxonomy.json")
    try:
        with open(data_path, "r") as f:
            taxonomy = json.load(f)
        return JSONResponse(content=taxonomy)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)}) 