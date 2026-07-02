import base64
import mimetypes
from pathlib import Path

import requests

from app.core.config import settings


def _is_configured(value: str | None) -> bool:
    return bool(value and value.strip() and not value.startswith("your_"))


class EmbeddingService:
    def embed_image_file(self, image_path: str | Path) -> list[float]:
        data_uri = self._image_file_to_data_uri(Path(image_path))
        return self.embed_image(data_uri)

    def embed_image(self, image: str) -> list[float]:
        return self._embed({"image": image})

    def embed_text(self, text: str) -> list[float]:
        return self._embed({"text": text})

    def _embed(self, content: dict[str, str]) -> list[float]:
        if not _is_configured(settings.ALIYUN_API_KEY):
            raise RuntimeError("ALIYUN_API_KEY is not configured.")

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
                        content,
                    ],
                },
                "parameters": {
                    "dimension": settings.ALIYUN_EMBEDDING_DIMENSION,
                },
            },
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        embeddings = data.get("output", {}).get("embeddings", [])
        if not embeddings:
            raise RuntimeError("Alibaba Cloud Bailian did not return embeddings.")

        vector = embeddings[0].get("embedding")
        if not isinstance(vector, list):
            raise RuntimeError("Alibaba Cloud Bailian returned invalid embedding payload.")

        if len(vector) != settings.ALIYUN_EMBEDDING_DIMENSION:
            raise RuntimeError(
                f"Embedding dimension mismatch: expected {settings.ALIYUN_EMBEDDING_DIMENSION}, got {len(vector)}."
            )
        return [float(value) for value in vector]

    @staticmethod
    def _image_file_to_data_uri(image_path: Path) -> str:
        mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"


embedding_service = EmbeddingService()
