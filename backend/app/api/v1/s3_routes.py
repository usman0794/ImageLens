from fastapi import APIRouter
import boto3

from app.config.settings import settings

router = APIRouter(
    prefix="/s3",
    tags=["AWS S3"]
)


@router.get("/test")
async def test_s3():

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    buckets = s3.list_buckets()

    return {
        "success": True,
        "bucket_count": len(buckets["Buckets"]),
        "buckets": [bucket["Name"] for bucket in buckets["Buckets"]],
    }