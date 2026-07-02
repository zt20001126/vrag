from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    designer_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    # pgvector stores this column as vector(512); raw SQL handles vector casts.
    embedding: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
