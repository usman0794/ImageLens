from app.config.settings import settings
from app.core.storage_service import LocalStorageService, S3StorageService
from app.repositories.image_repository import ImageRepository
from app.services.image_service import ImageService

# -----------------------------
# Lazy Singleton AI Components
# -----------------------------
# IMPORTANT: torch / transformers / faiss are heavy. We do NOT import them at
# module load and we do NOT build the model at import time. Instead we build the
# singletons on first use. This lets the web process boot and bind its port
# immediately (so Render detects an open port), and keeps idle memory low.

_clip_encoder = None
_faiss_store = None


def get_clip_encoder():
    global _clip_encoder
    if _clip_encoder is None:
        # Import here so transformers/torch are only loaded on first real use.
        from app.core.clip_encoder import CLIPEncoder
        _clip_encoder = CLIPEncoder()
    return _clip_encoder


def get_faiss_store():
    global _faiss_store
    if _faiss_store is None:
        # Import here so faiss is only loaded on first real use.
        from app.core.faiss_store import FAISSStore
        _faiss_store = FAISSStore()
    return _faiss_store

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

    The CLIP encoder and FAISS store are resolved lazily, so hitting a route
    that needs them is what triggers model loading — not server startup.
    """

    storage_service = get_storage_service()
    image_repository = ImageRepository()

    clip_encoder = get_clip_encoder()
    faiss_store = get_faiss_store()

    return ImageService(
        storage_service=storage_service,
        image_repository=image_repository,
        clip_encoder=clip_encoder,
        vector_store=faiss_store,
    )
