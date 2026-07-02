class PgVectorClient:
    def __init__(self, database_url: str | None = None) -> None:
        self.database_url = database_url

    def connect(self) -> None:
        # TODO: Initialize SQLAlchemy session or async database connection.
        return None

    def upsert_embedding(self, image_id: int, embedding: list[float]) -> None:
        # TODO: Persist image embedding into pgvector.
        return None

    def search(self, embedding: list[float], top_k: int = 5) -> list[dict[str, object]]:
        # TODO: Query pgvector for nearest images.
        return []
