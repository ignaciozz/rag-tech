from typing import List

from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.AI_API_KEY, base_url=settings.AI_BASE_URL or None)

# Precisa bater com a coluna document_chunks.embedding = Vector(1536) (models.py).
# Mudar isso exige recriar a coluna/tabela, não é só trocar aqui.
EMBEDDING_DIMENSIONS = 1536


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Gera um vetor de embedding para cada texto da lista, em uma única
    chamada à API (mais eficiente do que uma chamada por texto).
    """
    response = client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=texts,
        dimensions=EMBEDDING_DIMENSIONS,
    )

    # A API garante que response.data vem na mesma ordem dos textos enviados em `input`
    return [item.embedding for item in response.data]
