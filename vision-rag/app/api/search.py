from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.rag_service import rag_service


router = APIRouter()


class SearchRequest(BaseModel):
    query: str = Field(..., description="Text query for future multimodal retrieval.")
    designer_id: str | None = Field(default=None, description="Optional designer style filter.")
    top_k: int = Field(default=5, ge=1, le=50)


@router.post("/search")
async def search_images(request: SearchRequest) -> dict[str, object]:
    results = rag_service.search_similar_images(
        query=request.query,
        designer_id=request.designer_id,
        top_k=request.top_k,
    )
    return {
        "query": request.query,
        "designer_id": request.designer_id,
        "results": results,
    }
