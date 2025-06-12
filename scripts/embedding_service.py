import os
import openai
import asyncio
from typing import List
from config import Config

client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
EMBEDDING_MODEL = Config.EMBEDDING_MODEL_OPENAI
BATCH_SIZE = 1000  # OpenAI permite até 2048, mas 1000 é seguro

async def get_openai_embeddings(texts: List[str]) -> List[List[float]]:
    # OpenAI API não é async, então use run_in_executor para não travar event loop
    loop = asyncio.get_event_loop()
    embeddings = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i+BATCH_SIZE]
        try:
            response = await loop.run_in_executor(
                None,
                lambda: client.embeddings.create(
                    input=batch,
                    model=EMBEDDING_MODEL
                )
            )
            # Ordenar pelo index para garantir ordem
            batch_embeddings = [d.embedding for d in response.data]
            embeddings.extend(batch_embeddings)
        except Exception as e:
            print(f"[EmbeddingService] Erro ao obter embeddings do OpenAI: {e}")
            raise
    return embeddings 