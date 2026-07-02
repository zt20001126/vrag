from fastapi import UploadFile
import requests

from app.core.config import settings
from app.utils.file_utils import save_upload_file


def _is_configured(value: str | None) -> bool:
    return bool(value and value.strip() and not value.startswith("your_"))


class ImageService:
    def save_uploaded_image(self, file: UploadFile) -> str:
        return save_upload_file(file=file, upload_dir=settings.UPLOAD_DIR)

    def generate_image(self, prompt: str) -> dict[str, object]:
        if not _is_configured(settings.ALIYUN_API_KEY):
            return {
                "provider": "aliyun-bailian",
                "configured": False,
                "message": "ALIYUN_API_KEY is not configured.",
            }

        if not settings.ALIYUN_IMAGE_GENERATION_URL:
            return {
                "provider": "aliyun-bailian",
                "configured": True,
                "mode": "mock",
                "prompt": prompt,
                "image_url": "/static/mock-generated-image.png",
                "message": "ALIYUN_API_KEY configured. Set ALIYUN_IMAGE_GENERATION_URL to enable real call.",
            }

        try:
            headers = {
                "Authorization": f"Bearer {settings.ALIYUN_API_KEY}",
                "Content-Type": "application/json",
            }
            if "text2image/image-synthesis" in settings.ALIYUN_IMAGE_GENERATION_URL:
                headers["X-DashScope-Async"] = "enable"

            response = requests.post(
                settings.ALIYUN_IMAGE_GENERATION_URL,
                headers=headers,
                json={
                    "model": settings.ALIYUN_IMAGE_MODEL,
                    "input": {"prompt": prompt},
                },
                timeout=settings.REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            return {
                "provider": "aliyun-bailian",
                "configured": True,
                "success": False,
                "message": f"Alibaba Cloud Bailian request failed: {exc}",
            }

    def embed_image(self, image_url: str) -> dict[str, object]:
        if not _is_configured(settings.ALIYUN_API_KEY):
            return {
                "provider": "aliyun-bailian",
                "configured": False,
                "message": "ALIYUN_API_KEY is not configured.",
            }

        try:
            response = requests.post(
                settings.ALIYUN_EMBEDDING_API_URL,
                headers={
                    "Authorization": f"Bearer {settings.ALIYUN_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.ALIYUN_EMBEDDING_MODEL,
                    "input": {
                        "contents": [
                            {"image": image_url},
                        ],
                    },
                    "parameters": {
                        "dimension": settings.ALIYUN_EMBEDDING_DIMENSION,
                    },
                },
                timeout=settings.REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            return {
                "provider": "aliyun-bailian",
                "configured": True,
                "success": False,
                "message": f"Alibaba Cloud Bailian embedding request failed: {exc}",
            }


image_service = ImageService()
