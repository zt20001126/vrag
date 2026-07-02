from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from requests import RequestException
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import init_db
from app.services.rag_service import rag_service


router = APIRouter()


class SearchRequest(BaseModel):
    query: str = Field(..., description="Text query for future multimodal retrieval.")
    designer_id: int = Field(..., description="Designer style filter.")
    top_k: int = Field(default=5, ge=1, le=50)


@router.post("/search")
async def search_images(request: SearchRequest) -> dict[str, object]:
    try:
        init_db()
        results = rag_service.search_similar_images(
            query=request.query,
            designer_id=request.designer_id,
            top_k=request.top_k,
        )
    except (RequestException, RuntimeError, SQLAlchemyError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "query": request.query,
        "designer_id": request.designer_id,
        "results": results,
    }
