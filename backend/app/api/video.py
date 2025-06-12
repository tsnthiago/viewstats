from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse

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
    """Endpoint GET /video/{id} — retorna payload mockado do vídeo."""
    dummy_video = {
        "id": id,
        "title": "Exemplo de vídeo",
        "description": "Descrição do vídeo de exemplo.",
        "topics_path": ["Tecnologia > Programação > Python"],
        "channel_id": "canal123",
        "thumbnailUrl": "/placeholder.svg?height=225&width=400&text=Video",
        "duration": "10:23",
        "uploadDate": "2024-01-15",
        "viewCount": 125000,
        "language": "English",
        "tags": ["AI", "Machine Learning", "Technology", "Education"],
        "videoUrl": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
        "channel": {
            "id": "canal123",
            "name": "Canal Exemplo",
            "avatarUrl": "/placeholder.svg?height=40&width=40&text=CE"
        },
        "transcript": [
            {"id": "t1", "startTime": 0, "endTime": 5, "text": "Hello and welcome to our first video about AI."}
        ]
    }
    return JSONResponse(content=dummy_video) 