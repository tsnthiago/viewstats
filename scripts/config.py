import os

class Config:
    INPUT_CSV_PATH = 'input/input.csv'
    OUTPUT_JSON_PATH = 'data/processed_videos.json'
    DATA_DIR = 'data'
    SAMPLE_SIZE = 50
    TRANSCRIPT_MIN_LENGTH = 30
    TRANSCRIPT_MAX_CHARS = 4000
    API_KEY = os.getenv("GOOGLE_API_KEY")
    LLM_MODEL_VIDEO = "gemini-2.0-flash-lite"
    LLM_MODEL_TAXONOMY = "gemini-2.0-flash-lite"
    CONCURRENCY_LIMIT = 50
    LLM_VIDEO_INPUT_COST_PER_M = 0.075
    LLM_VIDEO_OUTPUT_COST_PER_M = 0.30
    LLM_TAXONOMY_INPUT_COST_PER_M = 0.075
    LLM_TAXONOMY_OUTPUT_COST_PER_M = 0.30
    QDRANT_URL = "http://147.79.111.195:6333"
    QDRANT_COLLECTION_NAME = "videos_viewstats"
    # EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
    EMBEDDING_MODEL = 'text-embedding-3-small'
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL_OPENAI = "text-embedding-3-small"
    EMBEDDING_COST_PER_M_TOKENS = 0.02