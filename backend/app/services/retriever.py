from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk
from app.services.embedder import generate_embeddings


def retrieve_relevant_chunks(db: Session, question: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Gera o embedding da pergunta e busca no pgvector os top_k chunks com
    menor distância de cosseno (ou seja, os mais parecidos semanticamente).
    """
    query_embedding = generate_embeddings([question])[0]

    distance = DocumentChunk.embedding.cosine_distance(query_embedding)

    results = (
        db.query(
            DocumentChunk.content,
            DocumentChunk.page_number,
            Document.title.label("document_title"),
            Document.technology,
            distance.label("distance"),
        )
        .join(Document, Document.id == DocumentChunk.document_id)
        .filter(DocumentChunk.embedding.is_not(None))
        .order_by(distance)
        .limit(top_k)
        .all()
    )

    return [
        {
            "content": row.content,
            "page_number": row.page_number,
            "document_title": row.document_title,
            "technology": row.technology,
            "distance": row.distance,
        }
        for row in results
    ]
