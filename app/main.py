from fastapi import FastAPI

from app.api import generate, search, upload
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="Image RAG knowledge base skeleton for designer style retrieval and image generation.",
)

app.include_router(upload.router, prefix=settings.API_PREFIX, tags=["upload"])
app.include_router(search.router, prefix=settings.API_PREFIX, tags=["search"])
app.include_router(generate.router, prefix=settings.API_PREFIX, tags=["generate"])


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.PROJECT_NAME}
