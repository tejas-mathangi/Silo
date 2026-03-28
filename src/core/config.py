from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Defines all base settings for the project. 

class Settings(BaseSettings):

    # Qdrant Configuration
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: str = "Silo_docs"

    # Embedding Configuration
    EMBEDDING_MODEL: str = "nomic-ai/nomic-embed-text-v1.5"
    EMBEDDING_DIMENSION: int = 768

    # LLM Configuration
    GROQ_API_KEY: Optional[str] = None
    OPEN_ROUTER_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    MISTRAL_API_KEY: Optional[str] = None
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    
    # LangSmith Observability
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: str = "silo-rag"

    # App Environment
    ENV: str = "development"  # Tells whether running in prod, or dev

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()