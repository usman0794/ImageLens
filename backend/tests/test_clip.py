from app.core.clip_encoder import CLIPEncoder

encoder = CLIPEncoder()

vector = encoder.encode_text("red sports car")

print("Vector shape:", vector.shape)
print("Vector type:", type(vector))
print("First 5 values:", vector[:5])