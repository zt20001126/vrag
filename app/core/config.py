from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "vision-rag")
    API_VERSION: str = os.getenv("API_VERSION", "0.1.0")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", "data/uploads"))

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://vision_rag:vision_rag_password@localhost:5432/vision_rag",
    )

    DEEPSEEK_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_URL: str = os.getenv(
        "DEEPSEEK_API_URL",
        "https://api.deepseek.com/chat/completions",
    )
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    ALIYUN_API_KEY: Optional[str] = os.getenv("ALIYUN_API_KEY")
    ALIYUN_EMBEDDING_API_URL: str = os.getenv(
        "ALIYUN_EMBEDDING_API_URL",
        "https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding",
    )
    ALIYUN_EMBEDDING_MODEL: str = os.getenv("ALIYUN_EMBEDDING_MODEL", "qwen3-vl-embedding")
    ALIYUN_EMBEDDING_DIMENSION: int = int(os.getenv("ALIYUN_EMBEDDING_DIMENSION", "512"))
    ALIYUN_IMAGE_GENERATION_URL: Optional[str] = os.getenv("ALIYUN_IMAGE_GENERATION_URL")
    ALIYUN_IMAGE_MODEL: str = os.getenv("ALIYUN_IMAGE_MODEL", "wanx2.1-t2i-turbo")

    REQUEST_TIMEOUT_SECONDS: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))


settings = Settings()
