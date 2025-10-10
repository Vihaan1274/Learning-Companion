import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API keys
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    # OpenRouter settings
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    OPENROUTER_MODEL = "alibaba/tongyi-deepresearch-30b-a3b:free"  # pick your model here
    SITE_URL = os.getenv("SITE_URL", "http://localhost")
    SITE_TITLE = os.getenv("SITE_TITLE", "AI Learning Companion")

    # Embedding model
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    # Retrieval
    TOP_K = 3
