import os
import uuid
from pathlib import Path

import boto3
from fastapi import UploadFile

from app.config.settings import settings


class LocalStorageService:
    """
    Local storage service.

    Used for development when STORAGE_TYPE=local.
    """

    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload_file(self, file: UploadFile) -> dict:
        file_extension = os.path.splitext(file.filename)[1]
        safe_filename = f"{uuid.uuid4().hex}{file_extension}"

        file_path = self.upload_dir / safe_filename

        content = await file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        file_size_kb = round(len(content) / 1024, 2)

        return {
            "filename": safe_filename,
            "url": f"/uploads/{safe_filename}",
            "path": str(file_path),
            "file_size_kb": file_size_kb,
            "storage_type": "local",
        }


class S3StorageService:
    """
    AWS S3 storage service.

    Used for production when STORAGE_TYPE=s3.
    """

    def __init__(self):
        self.bucket_name = settings.AWS_S3_BUCKET_NAME

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    async def save_upload_file(self, file: UploadFile) -> dict:
        file_extension = os.path.splitext(file.filename)[1]
        safe_filename = f"{uuid.uuid4().hex}{file_extension}"

        s3_key = f"uploads/{safe_filename}"

        content = await file.read()

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=content,
            ContentType=file.content_type,
        )

        file_size_kb = round(len(content) / 1024, 2)

        image_url = (
            f"https://{self.bucket_name}.s3."
            f"{settings.AWS_REGION}.amazonaws.com/{s3_key}"
        )

        return {
            "filename": safe_filename,
            "url": image_url,
            "path": image_url,
            "file_size_kb": file_size_kb,
            "storage_type": "s3",
        }