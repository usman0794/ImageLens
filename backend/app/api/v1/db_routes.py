from fastapi import APIRouter

from app.db.mongodb import MongoDB

router = APIRouter(
    prefix="/db",
    tags=["Database"]
)


@router.get("/test")
async def test_database():

    db = MongoDB.get_database()

    collections = await db.list_collection_names()

    return {
        "success": True,
        "message": "MongoDB Atlas Connected",
        "database": db.name,
        "collections": collections
    }