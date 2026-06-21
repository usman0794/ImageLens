import os
import faiss
import pickle
import numpy as np

from app.core.vector_store import VectorStore


class FAISSStore(VectorStore):
    def __init__(
        self,
        dimension: int = 512,
        index_path: str = "indexes/faiss.index",
        metadata_path: str = "indexes/vector_ids.pkl",
    ):
        self.dimension = dimension
        self.index_path = index_path
        self.metadata_path = metadata_path

        os.makedirs("indexes", exist_ok=True)

        print(f"[FAISSStore] index path: {os.path.abspath(self.index_path)}")

        self.vector_ids = []
        self.index = faiss.IndexFlatIP(self.dimension)

        if os.path.exists(index_path) and os.path.exists(metadata_path):
            try:
                self.load()
                print(f"[FAISSStore] Loaded index with {self.index.ntotal} vectors")

                if self.index.d != self.dimension:
                    print("⚠️ Dimension mismatch detected. Resetting index.")
                    self.index = faiss.IndexFlatIP(self.dimension)
                    self.vector_ids = []

            except Exception as e:
                print("⚠️ Failed to load FAISS index:", e)
                self.index = faiss.IndexFlatIP(self.dimension)
                self.vector_ids = []
        else:
            print("[FAISSStore] No existing index found, starting fresh.")

    def add_vector(self, vector_id: str, vector: np.ndarray):
        vector = np.asarray(vector, dtype=np.float32).reshape(1, -1)
        faiss.normalize_L2(vector)

        if vector.shape[1] != self.index.d:
            
            self.index = faiss.IndexFlatIP(vector.shape[1])
            self.dimension = vector.shape[1]
            self.vector_ids = []

        self.index.add(vector)
        self.vector_ids.append(vector_id)

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        query_vector = np.asarray(query_vector, dtype=np.float32).reshape(1, -1)
        faiss.normalize_L2(query_vector)

        

        if query_vector.shape[1] != self.index.d:
            
            return []

        if self.index.ntotal == 0:
            
            return []

        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append({
                "vector_id": self.vector_ids[idx],
                "score": float(score),
            })
        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.vector_ids, f)
        print(f"[FAISSStore] Saved index to {os.path.abspath(self.index_path)}")

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, "rb") as f:
            self.vector_ids = pickle.load(f)