from app.core.clip_encoder import CLIPEncoder
from app.core.faiss_store import FAISSStore


encoder = CLIPEncoder()

store = FAISSStore()

texts = [
    "red sports car",
    "blue motorcycle",
    "cute cat",
    "green tree",
]

for text in texts:
    vector = encoder.encode_text(text)

    store.add_vector(
        vector_id=text,
        vector=vector,
    )

store.save()

query_vector = encoder.encode_text(
    "fast red vehicle"
)

results = store.search(
    query_vector,
    top_k=3,
)

print(results)