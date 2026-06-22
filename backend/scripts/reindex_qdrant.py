"""
One-time backfill: re-index every image already in MongoDB into Qdrant.

The old FAISS index lived in memory and was wiped on restart, so this rebuilds
the vector index from your durable MongoDB records. For each image it fetches
the file from its stored URL, re-encodes it via the CLIP service, and upserts
the vector into Qdrant.

Run locally from the backend/ folder, using the same .env as the backend
(must have MONGODB_URL, MONGODB_DB_NAME, CLIP_SERVICE_URL, QDRANT_URL,
QDRANT_API_KEY set):

    python -m scripts.reindex_qdrant
"""

import requests
from pymongo import MongoClient

from app.config.settings import settings
from app.core.clip_encoder import CLIPEncoder
from app.core.qdrant_store import QdrantStore


def main():
    client = MongoClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    images = db["images"]

    encoder = CLIPEncoder()
    store = QdrantStore(dimension=512, collection_name=settings.QDRANT_COLLECTION)

    total = images.count_documents({})
    print(f"Found {total} image(s) to re-index.")

    ok = 0
    failed = 0

    for doc in images.find({}):
        vector_id = doc.get("vector_id") or doc.get("image_id")
        url = doc.get("url")

        if not vector_id or not url:
            print(f"  skip: missing vector_id/url for {doc.get('_id')}")
            failed += 1
            continue

        try:
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()

            embedding = encoder.encode_image(resp.content)
            store.add_vector(vector_id=vector_id, vector=embedding)

            ok += 1
            print(f"  indexed {vector_id}")
        except Exception as e:
            failed += 1
            print(f"  FAILED {vector_id}: {e}")

    print(f"\nDone. Indexed {ok}, failed {failed}, total {total}.")
    print(f"Qdrant now holds {store.count()} vectors.")


if __name__ == "__main__":
    main()
