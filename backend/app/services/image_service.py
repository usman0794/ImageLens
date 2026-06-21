import uuid
from io import BytesIO

import boto3
import numpy as np
from botocore.config import Config
from PIL import Image
from fastapi import HTTPException

from app.config.settings import settings
from app.models.image_model import ImageCreate
from app.repositories.image_repository import ImageRepository


class ImageService:
    def __init__(
        self,
        storage_service,
        image_repository: ImageRepository,
        clip_encoder,
        vector_store,
    ):
        self.storage_service = storage_service
        self.image_repository = image_repository
        self.clip_encoder = clip_encoder
        self.vector_store = vector_store

    # =========================
    # S3 CLIENT
    # =========================
    def _get_s3_client(self):
        return boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            config=Config(signature_version="s3v4"),
        )

    # =========================
    # IMAGE DIMENSIONS
    # =========================
    def _get_image_dimensions(self, content: bytes):
        with Image.open(BytesIO(content)) as img:
            return img.size

    # =========================
    # PUBLIC / PRESIGNED IMAGE URL
    # =========================
    def _get_public_image_url(self, image_data: dict) -> str:
        """
        Return browser-readable image URL.

        If STORAGE_TYPE=s3, this returns a pre-signed URL so private S3
        objects can be displayed in the React frontend without making the
        bucket public.
        """

        filename = image_data.get("filename")
        stored_url = image_data.get("url") or image_data.get("path") or ""

        if filename and settings.STORAGE_TYPE == "s3":
            s3_key = f"uploads/{filename}"
            s3_client = self._get_s3_client()

            return s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": settings.AWS_S3_BUCKET_NAME,
                    "Key": s3_key,
                },
                ExpiresIn=3600,
            )

        if stored_url.startswith("http://") or stored_url.startswith("https://"):
            return (
                stored_url
                .replace(
                    "imagelens-s3.s3.us-east-1.amazonaws.com",
                    "imagelens-s3.s3.eu-north-1.amazonaws.com",
                )
                .replace(
                    "{https://imagelens-s3}.s3.eu-north-1.amazonaws.com",
                    "https://imagelens-s3.s3.eu-north-1.amazonaws.com",
                )
                .replace(
                    "{https://imagelens-s3}.s3.us-east-1.amazonaws.com",
                    "https://imagelens-s3.s3.eu-north-1.amazonaws.com",
                )
            )

        if stored_url.startswith("/uploads/") or stored_url.startswith("uploads/"):
            clean_path = stored_url.lstrip("/")
            return (
                "https://"
                + settings.AWS_S3_BUCKET_NAME
                + ".s3."
                + settings.AWS_REGION
                + ".amazonaws.com/"
                + clean_path
            )

        if filename:
            return "/uploads/" + filename

        return stored_url

    # =========================
    # NORMALIZE IMAGE RESPONSE
    # =========================
    def _to_image_response(self, image_data: dict, score=None) -> dict:
        return {
            "image_id": image_data.get("image_id"),
            "vector_id": image_data.get("vector_id"),
            "filename": image_data.get("filename"),
            "url": self._get_public_image_url(image_data),
            "score": score,
            "similarity": score,
            "storage_type": image_data.get("storage_type"),
            "source": image_data.get("source") or image_data.get("storage_type"),
            "tags": image_data.get("tags", []),
            "category": image_data.get("category"),
            "description": image_data.get("description"),
            "width": image_data.get("width"),
            "height": image_data.get("height"),
            "file_size_kb": image_data.get("file_size_kb"),
            "created_at": image_data.get("created_at"),
            "updated_at": image_data.get("updated_at"),
        }

    # =========================
    # SEARCH RESULT HYDRATION
    # =========================
    async def _hydrate_vector_results(self, raw_results: list) -> list:
        """
        Convert FAISS vector hits into frontend-ready image result objects.
        """

        results = []

        for hit in raw_results:
            vector_id = hit.get("vector_id")
            score = hit.get("score")

            if not vector_id:
                continue

            records = await self.image_repository.get_by_vector_ids([vector_id])

            if not records:
                continue

            image_data = records[0]

            results.append(
                self._to_image_response(
                    image_data=image_data,
                    score=score,
                )
            )

        return results

    # =========================
    # UPLOAD IMAGE PIPELINE
    # =========================
    async def upload_image(self, file, category=None, tags=None, description=None):
        try:
            image_id = f"img_{uuid.uuid4().hex[:12]}"
            vector_id = image_id

            content = await file.read()

            if not content:
                raise HTTPException(
                    status_code=400,
                    detail="Uploaded file is empty",
                )

            width, height = self._get_image_dimensions(content)

            await file.seek(0)

            saved_file = await self.storage_service.save_upload_file(file)

            embedding = self.clip_encoder.encode_image(content)
            embedding = np.array(embedding, dtype=np.float32).flatten()

            self.vector_store.add_vector(
                vector_id=vector_id,
                vector=embedding,
            )

            self.vector_store.save()

            image_data = ImageCreate(
                image_id=image_id,
                vector_id=vector_id,
                filename=saved_file["filename"],
                url=saved_file["url"],
                storage_type=saved_file.get("storage_type", settings.STORAGE_TYPE),
                source="user_upload",
                tags=tags or [],
                category=category,
                description=description,
                width=width,
                height=height,
                file_size_kb=saved_file["file_size_kb"],
            )

            data = image_data.model_dump(mode="json")

            await self.image_repository.create(data)

            return self._to_image_response(data)

        except HTTPException:
            raise

        except Exception as e:
            print(f"[UPLOAD ERROR] {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to upload image",
            )

    # =========================
    # IMAGE SEARCH
    # =========================
    async def search_similar_images(self, file, top_k=10):
        try:
            content = await file.read()

            if not content:
                raise HTTPException(
                    status_code=400,
                    detail="Search image is empty",
                )

            query_vector = self.clip_encoder.encode_image(content)
            query_vector = np.array(query_vector, dtype=np.float32).flatten()

            raw_results = self.vector_store.search(
                query_vector=query_vector,
                top_k=top_k,
            )

            if not raw_results:
                return []

            return await self._hydrate_vector_results(raw_results)

        except HTTPException:
            raise

        except Exception as e:
            print(f"[IMAGE SEARCH ERROR] {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to search image",
            )

    # =========================
    # TEXT SEARCH
    # =========================
    async def search_by_text(self, query: str, top_k: int = 10):
        try:
            query = (query or "").strip()

            if not query:
                raise HTTPException(
                    status_code=400,
                    detail="Search query is empty",
                )

            results_by_id = {}

            # 1. Exact keyword/tag/category/description search
            keyword_records = await self.image_repository.keyword_search(
                query=query,
                limit=top_k,
            )

            for image_data in keyword_records:
                image_id = image_data.get("image_id")

                if not image_id:
                    continue

                item = self._to_image_response(
                    image_data=image_data,
                    score=1.0,
                )

                item["match_type"] = "keyword"

                results_by_id[image_id] = item

            # 2. CLIP semantic text-to-image search
            if hasattr(self.clip_encoder, "encode_text"):
                query_vector = self.clip_encoder.encode_text(query)
                query_vector = np.array(
                    query_vector,
                    dtype=np.float32,
                ).flatten()

                raw_results = self.vector_store.search(
                    query_vector=query_vector,
                    top_k=top_k,
                )

                vector_results = await self._hydrate_vector_results(raw_results)

                for item in vector_results:
                    image_id = item.get("image_id")

                    if not image_id:
                        continue

                    if image_id not in results_by_id:
                        item["match_type"] = "semantic"
                        results_by_id[image_id] = item

            results = list(results_by_id.values())

            results.sort(
                key=lambda item: item.get("score") or 0,
                reverse=True,
            )

            return results[:top_k]

        except HTTPException:
            raise

        except Exception as e:
            print(f"[TEXT SEARCH ERROR] {e}")

            raise HTTPException(
                status_code=500,
                detail="Failed to search text",
            )


    # =========================
    # GET IMAGE BY ID
    # =========================
    async def get_image_by_id(self, image_id: str):
        try:
            image_data = await self.image_repository.get_by_image_id(image_id)

            if not image_data:
                raise HTTPException(
                    status_code=404,
                    detail="Image not found",
                )

            return self._to_image_response(image_data)

        except HTTPException:
            raise

        except Exception as e:
            print(f"[GET IMAGE ERROR] {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get image",
            )
