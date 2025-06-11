from pydantic import BaseModel, Field
from typing import Optional

class SearchRequest(BaseModel):
    """Modelo de request para busca semântica."""
    query: str = Field(..., example="Como usar FastAPI")
    topic_filter: Optional[str] = Field(None, example="Tecnologia > Programação > Python")
    top_k: int = Field(10, example=5, description="Número máximo de resultados") 