import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from app.api.v1.upload_routes import router as upload_router

from app.config.settings import settings
from app.db.mongodb import MongoDB
from app.api.v1.health_routes import router as health_router
from app.api.v1.db_routes import router as db_router
from app.api.v1.s3_routes import router as s3_router
from app.api.v1.search_routes import router as search_router
from app.api.v1.analytics_routes import router as analytics_router

from fastapi import Request
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):

    await MongoDB.connect()

    yield

    await MongoDB.close()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "ImageLens API running"}


app.include_router(
    health_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    db_router,
    prefix=settings.API_PREFIX
)

app.include_router(upload_router, prefix=settings.API_PREFIX)

app.include_router(
    s3_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    search_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    analytics_router,
    prefix=settings.API_PREFIX,
)


os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    print(f"[GLOBAL ERROR] {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error"
        }
    )