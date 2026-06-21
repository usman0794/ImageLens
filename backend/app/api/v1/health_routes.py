from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check():
    """
    Health check endpoint.

    Used to verify that the backend server is running.
    """

    return {
        "success": True,
        "message": "ImageLens backend is running",
        "model_loaded": False,
        "vector_store": "faiss",
    }