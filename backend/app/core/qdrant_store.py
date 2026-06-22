import uuid

import numpy as np

from app.config.settings import settings
from app.core.vector_store import VectorStore

# Fixed namespace so the same vector_id always maps to the same Qdrant point id.
_QDRANT_NAMESPACE = uuid.UUID("6f9619ff-8b86-d011-b42d-00cf4fc964ff")


class QdrantStore(VectorStore):
    """
    Persistent vector store backed by Qdrant Cloud.

    Unlike the in-memory FAISS index, Qdrant is an external running service, so
    vectors survive Render restarts and redeploys. This permanently fixes the
    "old images disappear after a restart" problem.

    It implements the same interface as FAISSStore (add_vector / search), so the
    business logic in image_service.py does not need to change.
    """

    def __init__(self, dimension: int = 512, collection_name: str | None = None):
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, VectorParams

        url = settings.QDRANT_URL
        api_key = settings.QDRANT_API_KEY

        if not url:
            raise RuntimeError(
                "QDRANT_URL environment variable is not set. Set it (and "
                "QDRANT_API_KEY) to your Qdrant Cloud cluster."
            )

        self.dimension = dimension
        self.collection_name = collection_name or settings.QDRANT_COLLECTION
        self.client = QdrantClient(url=url, api_key=api_key, timeout=60)

        # Create the collection once if it doesn't exist yet.
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.dimension,
                    distance=Distance.COSINE,
                ),
            )
            print(f"[QdrantStore] Created collection '{self.collection_name}'")
        else:
            print(
                f"[QdrantStore] Using existing collection '{self.collection_name}'"
            )

    # -------------------------
    # HELPERS
    # -------------------------
    def _point_id(self, vector_id: str) -> str:
        # Qdrant point ids must be an unsigned int or a UUID. Our app uses string
        # ids like "img_ab12cd34", so derive a deterministic UUID from them.
        # Deterministic => re-indexing the same image overwrites, never dupes.
        return str(uuid.uuid5(_QDRANT_NAMESPACE, vector_id))

    # -------------------------
    # VECTOR OPS
    # -------------------------
    def add_vector(self, vector_id: str, vector: np.ndarray):
        from qdrant_client.models import PointStruct

        vec = np.asarray(vector, dtype=np.float32).flatten().tolist()

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=self._point_id(vector_id),
                    vector=vec,
                    payload={"vector_id": vector_id},
                )
            ],
        )

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        vec = np.asarray(query_vector, dtype=np.float32).flatten().tolist()

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=vec,
            limit=top_k,
            with_payload=True,
        )

        results = []
        for point in response.points:
            payload = point.payload or {}
            vector_id = payload.get("vector_id")
            if vector_id is None:
                continue
            results.append(
                {
                    "vector_id": vector_id,
                    "score": float(point.score),
                }
            )
        return results

    # -------------------------
    # NO-OP PERSISTENCE
    # -------------------------
    # Qdrant persists every upsert immediately on the server, so these methods
    # exist only to satisfy the VectorStore interface and the existing call to
    # save() inside the upload pipeline.
    def save(self):
        pass

    def load(self):
        pass

    # -------------------------
    # OPTIONAL UTIL
    # -------------------------
    def count(self) -> int:
        return self.client.count(self.collection_name, exact=True).count
