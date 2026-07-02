class RagService:
    def search_similar_images(
        self,
        query: str,
        designer_id: str | None = None,
        top_k: int = 5,
    ) -> list[dict[str, object]]:
        # TODO: Embed query and retrieve similar images from pgvector.
        mock_results = [
            {
                "image_url": "/data/uploads/mock-image-001.png",
                "designer_id": designer_id or "mock-designer",
                "score": 0.98,
                "metadata": {"style": "minimal", "source": "mock"},
            },
            {
                "image_url": "/data/uploads/mock-image-002.png",
                "designer_id": designer_id or "mock-designer",
                "score": 0.93,
                "metadata": {"style": "editorial", "source": "mock"},
            },
        ]
        return mock_results[:top_k]


rag_service = RagService()
