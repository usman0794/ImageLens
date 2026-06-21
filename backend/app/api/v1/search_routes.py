from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel, Field

from app.dependencies.services import get_image_service
from app.services.image_service import ImageService


router = APIRouter(prefix="/search", tags=["Search"])


class TextSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language image search query")
    top_k: int = Field(default=10, ge=1, le=50, description="Maximum number of results")


@router.post("/image")
async def search_image(
    file: UploadFile = File(...),
    top_k: int = Form(10),
    image_service: ImageService = Depends(get_image_service),
):
    """
    Search indexed images using an uploaded image.
    """

    results = await image_service.search_similar_images(
        file=file,
        top_k=top_k,
    )

    return {
        "success": True,
        "count": len(results),
        "results": results,
    }


@router.post("/text")
async def search_text(
    request: TextSearchRequest,
    image_service: ImageService = Depends(get_image_service),
):
    """
    Search indexed images using natural language text.
    Example query: "red sports car", "office workspace", "wireless camera".
    """

    results = await image_service.search_by_text(
        query=request.query,
        top_k=request.top_k,
    )

    return {
        "success": True,
        "query": request.query,
        "count": len(results),
        "results": results,
    }
