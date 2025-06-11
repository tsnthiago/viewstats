from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Path

router = APIRouter()

@router.get(
    "/channel/{id}",
    summary="Recupera classificação de um canal",
    response_description="Classificação do canal",
    tags=["Canal"],
    description="""
    Retorna a classificação e tópicos principais de um canal, identificado por ID.
    """,
    responses={
        200: {
            "description": "Classificação do canal retornada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": "canal123",
                        "name": "Canal Exemplo",
                        "topics": ["Tecnologia > Programação", "Educação > Tutoriais"]
                    }
                }
            }
        }
    }
)
def get_channel(id: str = Path(..., description="ID do canal")):
    """Endpoint GET /channel/{id} — retorna classificação do canal (simulado)."""
    dummy_channel = {
        "id": id,
        "name": "Canal Exemplo",
        "topics": ["Tecnologia > Programação", "Educação > Tutoriais"]
    }
    return JSONResponse(content=dummy_channel) 