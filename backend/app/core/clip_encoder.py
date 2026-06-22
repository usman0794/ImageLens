# from PIL import Image
# from transformers import CLIPProcessor, CLIPModel
# import torch
# import numpy as np
# from io import BytesIO


# class CLIPEncoder:
#     """
#     Converts image/text into normalized CLIP embeddings.
#     """

#     def __init__(self):
#         self.model_name = "openai/clip-vit-base-patch32"

#         print("Loading CLIP model...")

#         self.model = CLIPModel.from_pretrained(self.model_name)
#         self.processor = CLIPProcessor.from_pretrained(self.model_name)

#         self.model.eval()

#         print(f"[CLIPEncoder] Model type: {type(self.model)}")
#         print("CLIP loaded successfully")

#     # -------------------------
#     # TEXT ENCODING
#     # -------------------------
#     def encode_text(self, text: str) -> np.ndarray:

#         inputs = self.processor(
#             text=[text],
#             return_tensors="pt",
#             padding=True,
#             truncation=True,
#         )

#         with torch.no_grad():
#             text_outputs = self.model.text_model(**inputs)
#             text_embeds = self.model.text_projection(text_outputs.pooler_output)

#         vector = text_embeds[0].cpu().numpy()
#         vector = vector / np.linalg.norm(vector)

#         print(f"[CLIPEncoder] text embedding shape: {vector.shape}")  # must be (512,)

#         return vector.astype("float32")

#     # -------------------------
#     # IMAGE ENCODING (BYTES)
#     # -------------------------
#     def encode_image(self, image_bytes: bytes) -> np.ndarray:

#         image = Image.open(BytesIO(image_bytes)).convert("RGB")

#         inputs = self.processor(images=image, return_tensors="pt")

#         with torch.no_grad():
#             vision_outputs = self.model.vision_model(**inputs)
#             image_embeds = self.model.visual_projection(vision_outputs.pooler_output)

#         vector = image_embeds[0].cpu().numpy()
#         vector = vector / np.linalg.norm(vector)

#         print(f"[CLIPEncoder] image embedding shape: {vector.shape}")  # must be (512,)

#         return vector.astype("float32")

import os
import tempfile
from io import BytesIO

import numpy as np
from PIL import Image


class CLIPEncoder:
    """
    CLIP encoder backed by ONNX (via fastembed) instead of PyTorch.

    Same public interface as before:
      - encode_text(text)  -> normalized float32 np.ndarray of shape (512,)
      - encode_image(bytes)-> normalized float32 np.ndarray of shape (512,)

    Why: PyTorch + fp32 CLIP needs ~600 MB RAM and cannot fit on a 512 MB
    Render instance. The ONNX runtime + a CLIP ONNX model is small enough to
    (tightly) fit, and removing torch/transformers also shrinks the build.

    The text and vision models below are projected into the SAME CLIP space,
    so image<->text cosine similarity works exactly like before.
    """

    def __init__(self):
        # Imported here (lazy) so the heavy model only loads on first use,
        # which lets the web process boot and bind its port immediately.
        from fastembed import ImageEmbedding, TextEmbedding

        print("Loading ONNX CLIP models (fastembed)...")

        self.text_model = TextEmbedding(model_name="Qdrant/clip-ViT-B-32-text")
        self.image_model = ImageEmbedding(model_name="Qdrant/clip-ViT-B-32-vision")

        print("CLIP (ONNX) loaded successfully")

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
        embedding = next(iter(self.text_model.embed([text])))
        vector = self._normalize(embedding)
        print(f"[CLIPEncoder] text embedding shape: {vector.shape}")  # (512,)
        return vector

    # -------------------------
    # IMAGE ENCODING (BYTES)
    # -------------------------
    def encode_image(self, image_bytes: bytes) -> np.ndarray:
        # fastembed's ImageEmbedding.embed reliably accepts file paths, so we
        # write the uploaded bytes to a short-lived temp file.
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            image.save(tmp, format="PNG")
            tmp_path = tmp.name

        try:
            embedding = next(iter(self.image_model.embed([tmp_path])))
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        vector = self._normalize(embedding)
        print(f"[CLIPEncoder] image embedding shape: {vector.shape}")  # (512,)
        return vector
