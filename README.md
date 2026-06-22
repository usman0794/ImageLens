# 🖼️ ImageLens

> Find images by **visual similarity** or **natural language** — a CLIP-powered reverse-image and text-to-image search engine.

Upload an image to find visually similar ones, or describe what you're looking for in plain English (e.g. *"a red sports car"*, *"office workspace at night"*) and ImageLens returns the closest matches from your indexed image library.

---

## 🌐 Live Demo

| Service | URL |
|---------|-----|
| **Frontend** (Vercel) | https://imagelens-io.vercel.app |
| **Backend API** (Render) | https://imagelens.onrender.com |
| **API Docs** (Swagger) | https://imagelens.onrender.com/docs |
| **CLIP Embedding Service** (Hugging Face Space) | https://usman0794-imagelens-clip.hf.space |

> ⏱️ **Note:** The backend (Render free tier) and the CLIP service (HF Space free tier) both sleep when idle. The **first request after inactivity can take ~30–60s** to wake up — subsequent requests are fast.

---

## ✨ Features

- 🔍 **Image-to-image search** — upload an image, get visually similar results ranked by cosine similarity.
- 💬 **Text-to-image search** — search your image library with natural language (cross-modal CLIP search).
- ⚡ **Fast vector search** — FAISS in-memory index for sub-second nearest-neighbor lookup.
- ☁️ **Cloud storage** — images stored in AWS S3 (or local disk in dev).
- 🧠 **Lightweight inference** — CLIP runs as ONNX via `fastembed` (no PyTorch), offloaded to a dedicated service so the API stays small.

---

## 🏗️ Architecture

ImageLens is split into **three independently deployed services** so each runs on a free tier:

```
   ┌─────────────────┐        ┌──────────────────────────┐        ┌────────────────────────┐
   │   Frontend      │        │        Backend API        │        │   CLIP Embedding       │
   │   React (SPA)   │  HTTPS │     FastAPI (Render)       │  HTTPS │   Service (HF Space)   │
   │   on Vercel     │ ─────► │                            │ ─────► │   fastembed + ONNX     │
   │                 │        │  • REST API (/api/v1)      │        │   CLIP ViT-B/32        │
   └─────────────────┘        │  • FAISS vector index      │        │   16 GB RAM            │
                              │  • MongoDB (metadata)      │        └────────────────────────┘
                              │  • AWS S3 (image files)    │
                              └──────────────────────────┘
                                    │            │
                            ┌───────┘            └────────┐
                            ▼                             ▼
                   ┌─────────────────┐          ┌──────────────────┐
                   │  MongoDB Atlas  │          │     AWS S3       │
                   │   (metadata)    │          │  (image files)   │
                   └─────────────────┘          └──────────────────┘
```

**Why three services?** CLIP ViT-B/32 needs more RAM than Render's 512 MB free tier allows. By moving the model to a free Hugging Face Space (16 GB RAM) and having the backend call it over HTTP, the entire stack runs **for free**. The backend stays light (FastAPI + FAISS + Mongo client + S3 client) and never loads the model itself.

### How a search works
1. User uploads an image (or types a query) in the frontend.
2. Frontend calls the backend (`POST /api/v1/search/image` or `/search/text`).
3. Backend forwards the image/text to the **CLIP service**, which returns a 512-dim normalized embedding.
4. Backend runs a **FAISS** nearest-neighbor search over the indexed image vectors.
5. Backend fetches matching image metadata from **MongoDB** and S3 URLs, and returns ranked results.

---

## 🧰 Tech Stack

### Backend
- **FastAPI** + **Uvicorn** — async REST API
- **MongoDB** (via **Motor** / **PyMongo**) — image metadata
- **FAISS** (`faiss-cpu`) — vector similarity index
- **AWS S3** (via **boto3**) — image file storage
- **Pydantic v2** / **pydantic-settings** — config & validation
- **requests** — calls the CLIP service

### CLIP Service (Hugging Face Space)
- **FastAPI** (Docker SDK Space)
- **fastembed** — CLIP **ViT-B/32** via **ONNX Runtime** (no PyTorch)
- Models: `Qdrant/clip-ViT-B-32-text` and `Qdrant/clip-ViT-B-32-vision`

### Frontend
- **React** single-page app
- Deployed on **Vercel**

### Infrastructure
- **Render** — backend hosting
- **Vercel** — frontend hosting
- **Hugging Face Spaces** — CLIP inference
- **MongoDB Atlas** — managed database
- **AWS S3** — object storage

---

## 📁 Repository Structure

```
ImageLens/
├── backend/                  # FastAPI backend (deployed on Render, root dir = backend)
│   ├── app/
│   │   ├── main.py           # App entry, router registration, CORS
│   │   ├── config/
│   │   │   └── settings.py    # Env-driven settings (API_PREFIX, Mongo, S3, CORS...)
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── health_routes.py   # GET /health
│   │   │       └── search_routes.py   # POST /search/image, /search/text
│   │   ├── core/
│   │   │   ├── clip_encoder.py # HTTP client → CLIP service
│   │   │   ├── faiss_store.py  # FAISS index wrapper
│   │   │   └── storage_service.py # Local / S3 storage
│   │   ├── dependencies/
│   │   │   └── services.py     # Lazy singletons (encoder, faiss, storage)
│   │   ├── repositories/
│   │   │   └── image_repository.py # Mongo data access
│   │   └── services/
│   │       └── image_service.py    # Upload + search business logic
│   ├── requirements.txt
│   └── runtime.txt           # Python version pin
│
├── client/                   # React frontend (deployed on Vercel)
│   ├── src/
│   ├── public/
│   └── package.json
│
└── clip-space/               # CLIP embedding service (deployed on Hugging Face Space)
    ├── app.py                # FastAPI: /embed/text, /embed/image
    ├── requirements.txt
    ├── Dockerfile
    └── README.md             # HF Space config (sdk: docker, app_port: 7860)
```

---

## 🔌 API Reference

Base URL: `https://imagelens.onrender.com/api/v1`

### Health
```http
GET /api/v1/health/
```
Returns service status.

### Upload & index an image
```http
POST /api/v1/images/upload
Content-Type: multipart/form-data

file=<image>
```
Stores the image (S3), computes its CLIP embedding, and adds it to the FAISS index.

### Search by image
```http
POST /api/v1/search/image
Content-Type: multipart/form-data

file=<image>
top_k=10
```
**Response**
```json
{ "success": true, "count": 10, "results": [ /* ranked matches */ ] }
```

### Search by text
```http
POST /api/v1/search/text
Content-Type: application/json

{ "query": "a red bicycle", "top_k": 10 }
```
**Response**
```json
{ "success": true, "query": "a red bicycle", "count": 10, "results": [ /* ranked matches */ ] }
```

Full interactive docs: **https://imagelens.onrender.com/docs**

---

## 🚀 Local Development

### Prerequisites
- Python 3.12
- Node.js 18+
- A MongoDB connection string (MongoDB Atlas free tier works)
- (Optional) AWS S3 bucket — or use `STORAGE_TYPE=local`

### 1. CLIP service (run locally or use the deployed Space)
```bash
cd clip-space
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860
# → http://localhost:7860/docs
```

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# create a .env file (see Environment Variables below), then:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# → http://localhost:8000/docs
```

### 3. Frontend
```bash
cd client
npm install

# create .env with the API base URL (see below), then:
npm run dev
```

---

## 🔐 Environment Variables

### Backend (Render)
| Variable | Required | Example / Notes |
|----------|----------|-----------------|
| `MONGODB_URL` | ✅ | `mongodb+srv://user:pass@cluster.mongodb.net` |
| `MONGODB_DB_NAME` | ✅ | `imagelens` |
| `CLIP_SERVICE_URL` | ✅ | `https://usman0794-imagelens-clip.hf.space` (no trailing slash) |
| `STORAGE_TYPE` | ✅ | `s3` (prod) or `local` (dev) |
| `AWS_ACCESS_KEY_ID` | s3 only | AWS IAM key |
| `AWS_SECRET_ACCESS_KEY` | s3 only | AWS IAM secret |
| `AWS_REGION` | s3 only | e.g. `eu-north-1` |
| `AWS_S3_BUCKET_NAME` | s3 only | your bucket name |
| `CORS_ORIGINS` | ✅ | `https://imagelens-io.vercel.app` (comma-separate multiple) |
| `CLIP_SERVICE_TIMEOUT` | optional | seconds; default `120` (covers Space cold start) |

### Frontend (Vercel)
Set the API base URL to include the `/api/v1` prefix. Use the variable name matching your framework:
```
# Vite
VITE_API_BASE_URL=https://imagelens.onrender.com/api/v1
# Next.js
NEXT_PUBLIC_API_BASE_URL=https://imagelens.onrender.com/api/v1
# Create React App
REACT_APP_API_BASE_URL=https://imagelens.onrender.com/api/v1
```

### CLIP Service (Hugging Face Space)
No required variables. Optional:
| Variable | Notes |
|----------|-------|
| `FASTEMBED_CACHE` | model cache dir (defaults to `/tmp/fastembed`) |

---

## ☁️ Deployment

### Backend → Render
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Set all backend env vars above. Keep a **single worker** (free tier RAM).

### CLIP Service → Hugging Face Space
- Create a **Docker** Space, upload `app.py`, `requirements.txt`, `Dockerfile`, `README.md`.
- It auto-builds and serves on port `7860`.

### Frontend → Vercel
- Import the repo, set **Root Directory** to `client`.
- Add the API base URL env var (above) and deploy.

---

## 📜 License

MIT — feel free to use and adapt.

---

## 🙌 Acknowledgements

- [OpenAI CLIP](https://github.com/openai/CLIP) — the vision-language model
- [fastembed](https://github.com/qdrant/fastembed) — lightweight ONNX embeddings
- [FAISS](https://github.com/facebookresearch/faiss) — vector similarity search
