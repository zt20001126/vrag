from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    image_url: Mapped[str] = mapped_column(String(512), nullable=False)
    designer_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    # TODO: Replace JSON placeholder with pgvector Vector type when database integration is added.
    embedding: Mapped[list[float] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
