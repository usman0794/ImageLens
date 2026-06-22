from app.config.settings import settings
from app.core.storage_service import LocalStorageService, S3StorageService
from app.repositories.image_repository import ImageRepository
from app.services.image_service import ImageService

# -----------------------------
# Lazy Singleton AI Components
# -----------------------------
# The CLIP encoder (remote HF Space client) and the vector store (Qdrant Cloud)
# are built on first use, not at import time. This lets the web process boot and
# bind its port immediately, and keeps idle memory low.

_clip_encoder = None
_vector_store = None


def get_clip_encoder():
    global _clip_encoder
    if _clip_encoder is None:
        from app.core.clip_encoder import CLIPEncoder

        _clip_encoder = CLIPEncoder()
    return _clip_encoder


def get_vector_store():
    global _vector_store
    if _vector_store is None:
        # Qdrant Cloud is a persistent external service, so the index survives
        # Render restarts and redeploys.
        from app.core.qdrant_store import QdrantStore

        _vector_store = QdrantStore(
            dimension=512,
            collection_name=settings.QDRANT_COLLECTION,
        )
    return _vector_store

# -----------------------------
# Storage Service
# -----------------------------


def get_storage_service():
    """
    Select storage service based on .env.

    STORAGE_TYPE=local → save in backend/uploads
    STORAGE_TYPE=s3    → save in AWS S3 bucket
    """

    if settings.STORAGE_TYPE == "s3":
        return S3StorageService()

    return LocalStorageService()

# -----------------------------
# Image Service
# -----------------------------


def get_image_service() -> ImageService:
    """
    Create ImageService with required dependencies.

    The CLIP encoder and vector store are resolved lazily, so hitting a route
    that needs them is what triggers their initialization — not server startup.
    """

    storage_service = get_storage_service()
    image_repository = ImageRepository()

    clip_encoder = get_clip_encoder()
    vector_store = get_vector_store()

    return ImageService(
        storage_service=storage_service,
        image_repository=image_repository,
        clip_encoder=clip_encoder,
        vector_store=vector_store,
    )
