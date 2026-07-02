from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from requests import RequestException
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import init_db
from app.services.image_service import image_service
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service


router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Prompt for future image generation.")
    designer_id: int = Field(..., description="Designer style reference.")
    top_k: int = Field(default=3, ge=1, le=10)


@router.post("/generate")
async def generate_image(request: GenerateRequest) -> dict[str, object]:
    try:
        init_db()
        references = rag_service.search_similar_images(
            query=request.prompt,
            designer_id=request.designer_id,
            top_k=request.top_k,
        )
        optimized = llm_service.optimize_prompt_with_references(
            prompt=request.prompt,
            reference_images=references,
        )
        optimized_prompt = str(optimized.get("content") or request.prompt)
        generation_result = image_service.generate_and_save_image(optimized_prompt)
    except (RequestException, RuntimeError, SQLAlchemyError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "message": "generation completed",
        "designer_id": request.designer_id,
        "original_prompt": request.prompt,
        "optimized_prompt": optimized_prompt,
        "references": references,
        "llm": {
            "provider": optimized.get("provider"),
            "configured": optimized.get("configured"),
            "model": optimized.get("model"),
        },
        "generation": generation_result,
        "generated_image_url": generation_result.get("local_image_url"),
    }
