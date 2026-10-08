import time
from typing import List

import openai
from openai import OpenAI

from app.core.config import settings
from app.core.exceptions import translate_openai_error

client = OpenAI(api_key=settings.AI_API_KEY, base_url=settings.AI_BASE_URL or None)

# Precisa bater com a coluna document_chunks.embedding = Vector(1536) (models.py).
# Mudar isso exige recriar a coluna/tabela, não é só trocar aqui.
EMBEDDING_DIMENSIONS = 1536

# O Gemini rejeita lotes com mais de 100 itens numa chamada de embedding
# (BatchEmbedContentsRequest) — mas o limite que mais importa na prática é
# outro: o tier gratuito tem 30.000 tokens/minuto. Chunks de ~500 tokens
# (ver chunker.py) fazem um lote de 100 passar fácil de 30k tokens numa
# chamada só, e isso NÃO se resolve com retry (a mesma chamada grande
# demais esbarra no teto de novo). 50 chunks × ~500 tokens ≈ 25k, com folga.
MAX_BATCH_SIZE = 50

# Mesmo com lotes menores, dois lotes seguidos na mesma janela de 1 minuto
# ainda podem somar mais que 30k tokens — por isso uma pausa curta entre
# lotes, e retry com backoff exponencial se mesmo assim bater rate limit.
MAX_RATE_LIMIT_RETRIES = 3
RETRY_BASE_DELAY_SECONDS = 2
INTER_BATCH_DELAY_SECONDS = 3


def _embed_batch(batch: List[str]) -> List[List[float]]:
    for attempt in range(MAX_RATE_LIMIT_RETRIES):
        try:
            response = client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=batch,
                dimensions=EMBEDDING_DIMENSIONS,
            )
            # A API garante que response.data vem na mesma ordem de `input`.
            return [item.embedding for item in response.data]
        except openai.RateLimitError as error:
            if attempt == MAX_RATE_LIMIT_RETRIES - 1:
                raise translate_openai_error(error) from error
            time.sleep(RETRY_BASE_DELAY_SECONDS * (2**attempt))
        except openai.APIError as error:
            # Outros erros (chave inválida, modelo inexistente...) não se
            # resolvem tentando de novo — falha na hora.
            raise translate_openai_error(error) from error

    raise AssertionError("inalcançável")  # loop sempre retorna ou lança antes


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Gera um vetor de embedding para cada texto da lista, em lotes de até
    MAX_BATCH_SIZE (uma chamada por lote, não uma por texto), com retry
    automático em caso de rate limit entre lotes.
    """
    all_embeddings: List[List[float]] = []
    batches = [texts[i : i + MAX_BATCH_SIZE] for i in range(0, len(texts), MAX_BATCH_SIZE)]

    for i, batch in enumerate(batches):
        if i > 0:
            time.sleep(INTER_BATCH_DELAY_SECONDS)
        all_embeddings.extend(_embed_batch(batch))

    return all_embeddings
