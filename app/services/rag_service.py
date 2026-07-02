from app.services.embedding_service import embedding_service
from app.vector.client import pgvector_client


class RagService:
    def search_similar_images(
        self,
        query: str,
        designer_id: int,
        top_k: int = 5,
    ) -> list[dict[str, object]]:
        query_embedding = embedding_service.embed_text(query)
        return pgvector_client.search(
            embedding=query_embedding,
            designer_id=designer_id,
            top_k=top_k,
        )


rag_service = RagService()
