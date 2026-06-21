from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch
import numpy as np
from io import BytesIO


class CLIPEncoder:
    """
    Converts image/text into normalized CLIP embeddings.
    """

    def __init__(self):
        self.model_name = "openai/clip-vit-base-patch32"

        print("Loading CLIP model...")

        self.model = CLIPModel.from_pretrained(self.model_name)
        self.processor = CLIPProcessor.from_pretrained(self.model_name)

        self.model.eval()

        print(f"[CLIPEncoder] Model type: {type(self.model)}")
        print("CLIP loaded successfully")

    # -------------------------
    # TEXT ENCODING
    # -------------------------
    def encode_text(self, text: str) -> np.ndarray:

        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True,
            truncation=True,
        )

        with torch.no_grad():
            text_outputs = self.model.text_model(**inputs)
            text_embeds = self.model.text_projection(text_outputs.pooler_output)

        vector = text_embeds[0].cpu().numpy()
        vector = vector / np.linalg.norm(vector)

        print(f"[CLIPEncoder] text embedding shape: {vector.shape}")  # must be (512,)

        return vector.astype("float32")

    # -------------------------
    # IMAGE ENCODING (BYTES)
    # -------------------------
    def encode_image(self, image_bytes: bytes) -> np.ndarray:

        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            vision_outputs = self.model.vision_model(**inputs)
            image_embeds = self.model.visual_projection(vision_outputs.pooler_output)

        vector = image_embeds[0].cpu().numpy()
        vector = vector / np.linalg.norm(vector)

        print(f"[CLIPEncoder] image embedding shape: {vector.shape}")  # must be (512,)

        return vector.astype("float32")