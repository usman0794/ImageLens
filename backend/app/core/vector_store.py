from abc import ABC, abstractmethod
import numpy as np


class VectorStore(ABC):
    """
    Abstract vector store interface.

    Allows switching between:
    - FAISS
    - Qdrant
    - Pinecone
    without changing business logic.
    """

    @abstractmethod
    def add_vector(self, vector_id: str, vector: np.ndarray):
        pass

    @abstractmethod
    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 5
    ):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass