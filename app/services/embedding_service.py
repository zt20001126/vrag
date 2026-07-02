class EmbeddingService:
    def embed_image(self, image_path: str) -> list[float] | None:
        # TODO: Integrate CLIP or another vision embedding model.
        return None

    def embed_text(self, text: str) -> list[float] | None:
        # TODO: Integrate CLIP or another text embedding model.
        return None


embedding_service = EmbeddingService()
