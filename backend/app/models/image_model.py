from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ImageCreate(BaseModel):
    """
    Data needed when saving a newly uploaded image.
    """

    image_id: str
    vector_id: str
    filename: str
    url: str
    storage_type: str = "local"
    source: str = "user_upload"
    tags: List[str] = []
    category: Optional[str] = None
    description: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    file_size_kb: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ImageResponse(BaseModel):
    """
    Image response returned to frontend.
    """

    image_id: str
    vector_id: str
    filename: str
    url: str
    storage_type: str
    source: str
    tags: List[str]
    category: Optional[str]
    description: Optional[str]
    width: Optional[int]
    height: Optional[int]
    file_size_kb: Optional[float] = None
    created_at: datetime