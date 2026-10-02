from typing import List

from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Mesmo modelo usado no encoding do chunker (cl100k_base) e compatível com Vector(1536)
EMBEDDING_MODEL = "text-embedding-3-small"


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Gera um vetor de embedding para cada texto da lista, em uma única
    chamada à API da OpenAI (mais eficiente do que uma chamada por texto).
    """
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)

    # A API garante que response.data vem na mesma ordem dos textos enviados em `input`
    return [item.embedding for item in response.data]
