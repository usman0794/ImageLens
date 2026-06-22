from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from .env file.

    SOLID:
    - Single Responsibility: this class only manages environment configuration.
    """

    APP_NAME: str = "ImageLens API"
    APP_ENV: str = "development"
    API_PREFIX: str = "/api/v1"

    MONGODB_URL: str
    MONGODB_DB_NAME: str

    VECTOR_STORE: str = "faiss"
    STORAGE_TYPE: str = "local"

    UPLOAD_DIR: str = "uploads"
    INDEX_DIR: str = "indexes"
    MODEL_CACHE_DIR: str = "models_cache"

    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_REGION: str | None = None
    AWS_S3_BUCKET_NAME: str | None = None


    # ===== Qdrant Cloud (vector database) =====
    QDRANT_URL: str | None = None
    QDRANT_API_KEY: str | None = None
    QDRANT_COLLECTION: str = "images"

    class Config:
        env_file = ".env"
        extra = "ignore" 


settings = Settings()