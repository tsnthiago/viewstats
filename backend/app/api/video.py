from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Path

router = APIRouter()

@router.get(
    "/video/{id}",
    summary="Recupera metadados de um vídeo",
    response_description="Payload do vídeo",
    tags=["Vídeo"],
    description="""
    Retorna os metadados e tópicos de um vídeo específico, identificado por ID.
    """,
    responses={
        200: {
            "description": "Metadados do vídeo retornados com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": "abc123",
                        "title": "Exemplo de vídeo",
                        "description": "Descrição do vídeo de exemplo.",
                        "topics_path": ["Tecnologia > Programação > Python"],
                        "channel_id": "canal123"
                    }
                }
            }
        }
    }
)
def get_video(id: str = Path(..., description="ID do vídeo")):
    """Endpoint GET /video/{id} — retorna payload do vídeo no Qdrant (simulado)."""
    # Simulação de resposta
    dummy_video = {
        "id": id,
        "title": "Exemplo de vídeo",
        "description": "Descrição do vídeo de exemplo.",
        "topics_path": ["Tecnologia > Programação > Python"],
        "channel_id": "canal123"
    }
    return JSONResponse(content=dummy_video) 