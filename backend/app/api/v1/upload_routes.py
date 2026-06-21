from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.dependencies.services import get_image_service
from app.services.image_service import ImageService
from fastapi import HTTPException

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    category: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image_service: ImageService = Depends(get_image_service)
):

    """
    Upload and save image metadata.

    Current MVP:
    - Save image locally
    - Save metadata to MongoDB

    Next:
    - Generate CLIP vector
    - Save vector to FAISS
    """

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed"
        )
    
    tag_list = []

    if tags:
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]

    uploaded_image = await image_service.upload_image(
        file=file,
        category=category,
        tags=tag_list,
        description=description
    )

    return {
        "success": True,
        "message": "Image uploaded successfully",
        "image": uploaded_image
    }