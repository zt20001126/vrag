from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.image_service import image_service


router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Prompt for future image generation.")
    designer_id: str | None = Field(default=None, description="Optional designer style reference.")


@router.post("/generate")
async def generate_image(request: GenerateRequest) -> dict[str, object]:
    result = image_service.generate_image(request.prompt)
    result["designer_id"] = request.designer_id
    return result
