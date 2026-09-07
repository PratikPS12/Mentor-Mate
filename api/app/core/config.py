from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="allow")

    PROJECT_NAME: str = "Mentor Mate API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Security
    JWT_SECRET: str = "mentor_mate_super_secret_jwt_key_2026_adaptive_learning"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # MongoDB Atlas Configuration
    MONGODB_URI: Optional[str] = None
    DATABASE_NAME: str = "mentor_mate_db"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]
    
    # Upload storage
    UPLOAD_DIR: str = "data/uploads"

    # AI Provider & AgentRouter Configuration
    AI_PROVIDER: str = "agentrouter"
    AGENTROUTER_BASE_URL: str = "https://co.agentrouter.org/v1"
    AGENTROUTER_API_KEY: Optional[str] = None

    # Model Routing Configuration
    AI_MODEL_PRIMARY: str = "gpt-4o"
    AI_MODEL_FAST: str = "gpt-4o-mini"
    AI_MODEL_REASONING: str = "o1"
    AI_MODEL_VISION: str = "gpt-4o"
    AI_MODEL_FALLBACK: str = "gpt-4o-mini"

    # Embeddings
    EMBEDDING_PROVIDER: str = "openai"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

settings = Settings()

