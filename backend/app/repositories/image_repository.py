from typing import List, Optional

from app.db.collections import Collections
from app.db.mongodb import MongoDB


class ImageRepository:
    """
    Handles only MongoDB operations for image metadata.
    """

    def __init__(self):
        db = MongoDB.get_database()
        self.collection = db[Collections.IMAGES]

    async def create(self, image_data: dict) -> str:
        # Copy data before inserting because MongoDB adds _id into the dict
        data_to_insert = image_data.copy()

        result = await self.collection.insert_one(data_to_insert)

        return str(result.inserted_id)

    async def get_by_image_id(self, image_id: str) -> Optional[dict]:
        return await self.collection.find_one(
            {"image_id": image_id},
            {"_id": 0}
        )

    async def get_by_vector_ids(self, vector_ids: List[str]) -> List[dict]:
        cursor = self.collection.find(
            {"vector_id": {"$in": vector_ids}},
            {"_id": 0}
        )
        return await cursor.to_list(length=len(vector_ids))

    async def count_all(self) -> int:
        return await self.collection.count_documents({})
    
    async def keyword_search(self, query: str, limit: int = 10) -> List[dict]:
        query = query.strip()

        if not query:
            return []

        regex = {
            "$regex": query,
            "$options": "i"
        }

        cursor = self.collection.find(
            {
                "$or": [
                    {"filename": regex},
                    {"category": regex},
                    {"description": regex},
                    {"tags": regex},
                ]
            },
            {"_id": 0}
        ).limit(limit)

        return await cursor.to_list(length=limit)