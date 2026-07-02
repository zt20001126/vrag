from sqlalchemy import text

from app.db.session import SessionLocal


class PgVectorClient:
    def create_image(
        self,
        image_url: str,
        designer_id: int,
        embedding: list[float],
    ) -> dict[str, object]:
        vector_literal = self._to_vector_literal(embedding)
        with SessionLocal() as session:
            row = session.execute(
                text(
                    """
                    INSERT INTO images (image_url, designer_id, embedding)
                    VALUES (:image_url, :designer_id, CAST(:embedding AS vector))
                    RETURNING id, image_url, designer_id, created_at
                    """
                ),
                {
                    "image_url": image_url,
                    "designer_id": designer_id,
                    "embedding": vector_literal,
                },
            ).mappings().one()
            session.commit()
            return dict(row)

    def search(
        self,
        embedding: list[float],
        designer_id: int,
        top_k: int = 5,
    ) -> list[dict[str, object]]:
        vector_literal = self._to_vector_literal(embedding)
        with SessionLocal() as session:
            rows = session.execute(
                text(
                    """
                    SELECT
                        id,
                        image_url,
                        designer_id,
                        created_at,
                        embedding <=> CAST(:embedding AS vector) AS distance
                    FROM images
                    WHERE designer_id = :designer_id
                      AND embedding IS NOT NULL
                    ORDER BY embedding <=> CAST(:embedding AS vector)
                    LIMIT :top_k
                    """
                ),
                {
                    "embedding": vector_literal,
                    "designer_id": designer_id,
                    "top_k": top_k,
                },
            ).mappings().all()
        return [self._format_search_row(row) for row in rows]

    @staticmethod
    def _to_vector_literal(embedding: list[float]) -> str:
        return "[" + ",".join(str(float(value)) for value in embedding) + "]"

    @staticmethod
    def _format_search_row(row: object) -> dict[str, object]:
        data = dict(row)
        distance = float(data["distance"])
        data["distance"] = distance
        data["score"] = max(0.0, 1.0 - distance)
        data["created_at"] = data["created_at"].isoformat()
        return data


pgvector_client = PgVectorClient()
