from app.config.settings import settings
from app.core.storage_service import LocalStorageService, S3StorageService

from app.core.clip_encoder import CLIPEncoder
from app.core.faiss_store import FAISSStore
from app.repositories.image_repository import ImageRepository
from app.services.image_service import ImageService

# -----------------------------
# Singleton AI Components
# -----------------------------

clip_encoder = CLIPEncoder()
faiss_store = FAISSStore()


def get_clip_encoder():
    return clip_encoder


def get_faiss_store():
    return faiss_store

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
    """

    storage_service = get_storage_service()
    image_repository = ImageRepository()

    clip_encoder = get_clip_encoder()
    faiss_store = get_faiss_store()

    return ImageService(
        storage_service=storage_service,
        image_repository=image_repository,
        clip_encoder=clip_encoder,
        vector_store=faiss_store
    )