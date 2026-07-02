from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Prompt for future image generation.")
    designer_id: str | None = Field(default=None, description="Optional designer style reference.")


@router.post("/generate")
async def generate_image(request: GenerateRequest) -> dict[str, str | None]:
    # TODO: Replace with Stable Diffusion or another image generation backend.
    return {
        "message": "mock image generated",
        "prompt": request.prompt,
        "designer_id": request.designer_id,
        "image_url": "/static/mock-generated-image.png",
    }
