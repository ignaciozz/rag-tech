import openai
import pytest

from app.core.exceptions import AIProviderError
from app.services.embedder import EMBEDDING_DIMENSIONS, generate_embeddings


def test_generate_embeddings_retorna_um_vetor_por_texto(mock_embeddings):
    fake_vector = mock_embeddings(dimensions=EMBEDDING_DIMENSIONS)

    result = generate_embeddings(["primeiro texto", "segundo texto"])

    assert len(result) == 2
    assert result[0] == fake_vector
    assert len(result[0]) == EMBEDDING_DIMENSIONS


def test_generate_embeddings_traduz_erro_de_autenticacao(monkeypatch):
    def fake_create(model, input, dimensions):
        raise openai.AuthenticationError(
            message="chave inválida",
            response=_fake_response(401),
            body=None,
        )

    from app.services import embedder
    monkeypatch.setattr(embedder.client.embeddings, "create", fake_create)

    with pytest.raises(AIProviderError, match="Chave de API"):
        generate_embeddings(["qualquer texto"])


def _fake_response(status_code):
    import httpx
    return httpx.Response(status_code, request=httpx.Request("POST", "https://example.com"))
