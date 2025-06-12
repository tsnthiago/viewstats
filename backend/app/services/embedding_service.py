from openai import AsyncOpenAI
from app.core import config

OPENAI_API_KEY = config.OPENAI_API_KEY
EMBEDDING_MODEL = getattr(config, "EMBEDDING_MODEL_OPENAI", "text-embedding-3-small")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def get_openai_embeddings(texts: list[str]) -> list[list[float]]:
    results = []
    batch_size = 1000  # OpenAI API limit
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        try:
            response = await client.embeddings.create(
                input=batch,
                model=EMBEDDING_MODEL
            )
            # OpenAI returns embeddings in the same order as input
            results.extend([d.embedding for d in response.data])
        except Exception as e:
            print(f"[embedding_service] OpenAI embedding error: {e}")
            raise
    return results 