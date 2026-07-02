from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import generate, search, upload
from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="Image RAG knowledge base skeleton for designer style retrieval and image generation.",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(upload.router, prefix=settings.API_PREFIX, tags=["upload"])
app.include_router(search.router, prefix=settings.API_PREFIX, tags=["search"])
app.include_router(generate.router, prefix=settings.API_PREFIX, tags=["generate"])


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(BASE_DIR / "templates" / "index.html")


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.PROJECT_NAME}
