import io
import os

import numpy as np
import requests


class CLIPEncoder:
    """
    Thin HTTP client for a remote CLIP service (hosted on a free Hugging Face
    Space with 16 GB RAM). The Render web service stays light and never loads
    the model itself, so it fits comfortably in 512 MB.

    Same public interface as before:
      - encode_text(text)   -> normalized float32 np.ndarray of shape (512,)
      - encode_image(bytes) -> normalized float32 np.ndarray of shape (512,)

    Configure the service location with the CLIP_SERVICE_URL env var, e.g.
        CLIP_SERVICE_URL=https://<your-username>-imagelens-clip.hf.space
    """

    def __init__(self):
        base = os.environ.get("CLIP_SERVICE_URL", "").rstrip("/")
        if not base:
            raise RuntimeError(
                "CLIP_SERVICE_URL environment variable is not set. Point it at "
                "your Hugging Face Space, e.g. "
                "https://<username>-imagelens-clip.hf.space"
            )
        self.base_url = base
        # HF Spaces sleep when idle; the first call after a nap can take
        # ~30-60s to cold start, so use a generous timeout.
        self.timeout = float(os.environ.get("CLIP_SERVICE_TIMEOUT", "120"))
        print(f"CLIPEncoder -> remote CLIP service at {self.base_url}")

    # -------------------------
    # HELPERS
    # -------------------------
    def _normalize(self, vector) -> np.ndarray:
        vector = np.asarray(vector, dtype=np.float32).flatten()
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector.astype("float32")

    # -------------------------
    # TEXT ENCODING
    # -------------------------
    def encode_text(self, text: str) -> np.ndarray:
        resp = requests.post(
            f"{self.base_url}/embed/text",
            json={"text": text},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return self._normalize(resp.json()["embedding"])

    # -------------------------
    # IMAGE ENCODING (BYTES)
    # -------------------------
    def encode_image(self, image_bytes: bytes) -> np.ndarray:
        resp = requests.post(
            f"{self.base_url}/embed/image",
            files={"file": ("image.png", io.BytesIO(image_bytes), "image/png")},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return self._normalize(resp.json()["embedding"])
