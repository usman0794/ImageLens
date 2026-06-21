from fastapi import APIRouter

from app.db.collections import Collections
from app.db.mongodb import MongoDB


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/summary")
async def analytics_summary():
    """
    Dashboard analytics summary for frontend.

    Frontend calls:
    GET /api/v1/analytics/summary
    """

    db = MongoDB.get_database()

    images_collection = db[Collections.IMAGES]
    search_history_collection = db[Collections.SEARCH_HISTORY]

    # -------------------------
    # Total images
    # -------------------------
    total_images = await images_collection.count_documents({})

    # -------------------------
    # Unique categories
    # -------------------------
    categories = await images_collection.distinct(
        "category",
        {
            "category": {
                "$nin": [None, ""],
            }
        },
    )

    total_categories = len(categories)

    # -------------------------
    # Search count
    # -------------------------
    try:
        total_searches = await search_history_collection.count_documents({})
    except Exception:
        total_searches = 0

    # -------------------------
    # Average latency
    # -------------------------
    avg_latency = 0

    try:
        latency_pipeline = [
            {
                "$match": {
                    "latency_ms": {
                        "$exists": True,
                        "$ne": None,
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "avgLatency": {
                        "$avg": "$latency_ms",
                    },
                }
            },
        ]

        latency_result = await search_history_collection.aggregate(
            latency_pipeline
        ).to_list(length=1)

        if latency_result:
            avg_latency = round(
                latency_result[0].get("avgLatency", 0),
                2,
            )

    except Exception:
        avg_latency = 0

    # -------------------------
    # Top categories
    # -------------------------
    top_categories = []

    try:
        top_categories_pipeline = [
            {
                "$match": {
                    "category": {
                        "$nin": [None, ""],
                    }
                }
            },
            {
                "$group": {
                    "_id": "$category",
                    "count": {
                        "$sum": 1,
                    },
                }
            },
            {
                "$sort": {
                    "count": -1,
                }
            },
            {
                "$limit": 5,
            },
        ]

        category_rows = await images_collection.aggregate(
            top_categories_pipeline
        ).to_list(length=5)

        top_categories = [
            {
                "category": row["_id"],
                "count": row["count"],
            }
            for row in category_rows
        ]

    except Exception:
        top_categories = []

    # -------------------------
    # Searches over time
    # -------------------------
    # This stays empty until you store search history documents.
    searches_over_time = []

    return {
        "success": True,
        "metrics": {
            "totalImages": total_images,
            "searches": total_searches,
            "categories": total_categories,
            "avgLatency": avg_latency,
        },
        "searchesOverTime": searches_over_time,
        "topCategories": top_categories,
    }
