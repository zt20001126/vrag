import time
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
import requests

from app.core.config import settings
from app.services.embedding_service import embedding_service
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

    def generate_and_save_image(self, prompt: str) -> dict[str, object]:
        creation_result = self.generate_image(prompt)
        task_id = creation_result.get("output", {}).get("task_id")
        if not task_id:
            return creation_result

        task_result = self.wait_for_image_task(str(task_id))
        image_url = self._extract_generated_image_url(task_result)
        if not image_url:
            task_result["local_image_url"] = None
            return task_result

        local_url = self.download_generated_image(image_url)
        task_result["remote_image_url"] = image_url
        task_result["local_image_url"] = local_url
        return task_result

    def wait_for_image_task(self, task_id: str) -> dict[str, object]:
        deadline = time.monotonic() + settings.IMAGE_TASK_MAX_WAIT_SECONDS
        last_result: dict[str, object] = {}
        while time.monotonic() < deadline:
            last_result = self.get_image_task(task_id)
            status = last_result.get("output", {}).get("task_status")
            if status in {"SUCCEEDED", "FAILED", "UNKNOWN"}:
                return last_result
            time.sleep(settings.IMAGE_TASK_POLL_INTERVAL_SECONDS)

        last_result["success"] = False
        last_result["message"] = "Image generation task polling timed out."
        return last_result

    def get_image_task(self, task_id: str) -> dict[str, object]:
        response = requests.get(
            f"{settings.ALIYUN_IMAGE_TASK_URL_PREFIX}/{task_id}",
            headers={"Authorization": f"Bearer {settings.ALIYUN_API_KEY}"},
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()

    def download_generated_image(self, remote_image_url: str) -> str:
        settings.GENERATED_DIR.mkdir(parents=True, exist_ok=True)
        response = requests.get(remote_image_url, timeout=settings.REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()

        suffix = self._guess_image_suffix(remote_image_url, response.headers.get("Content-Type"))
        file_name = f"{uuid4().hex}{suffix}"
        target_path = settings.GENERATED_DIR / file_name
        target_path.write_bytes(response.content)
        return f"{settings.GENERATED_ROUTE_PREFIX}/{file_name}"

    def embed_image(self, image_url: str) -> dict[str, object]:
        vector = embedding_service.embed_image(image_url)
        return {
            "provider": "aliyun-bailian",
            "configured": True,
            "embedding_dimension": len(vector),
            "embedding_preview": vector[:5],
        }

    @staticmethod
    def _extract_generated_image_url(task_result: dict[str, object]) -> str | None:
        output = task_result.get("output", {})
        if not isinstance(output, dict):
            return None
        results = output.get("results")
        if isinstance(results, list) and results:
            first = results[0]
            if isinstance(first, dict):
                return first.get("url")
        return output.get("url") if isinstance(output.get("url"), str) else None

    @staticmethod
    def _guess_image_suffix(remote_image_url: str, content_type: str | None) -> str:
        content_type_map = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
        }
        if content_type in content_type_map:
            return content_type_map[content_type]

        suffix = Path(remote_image_url.split("?")[0]).suffix.lower()
        return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp"} else ".png"


image_service = ImageService()
