from pydantic import BaseModel, Field
from typing import Optional

class SearchRequest(BaseModel):
    """Modelo de request para busca semântica."""
    query: str = Field(..., example="Como usar FastAPI")
    topic_filter: Optional[str] = Field(None, example="Tecnologia > Programação > Python")
    top_k: int = Field(10, example=5, description="Número máximo de resultados")
    page: Optional[int] = Field(1, example=1, description="Página de resultados")
    limit: Optional[int] = Field(10, example=10, description="Resultados por página") 