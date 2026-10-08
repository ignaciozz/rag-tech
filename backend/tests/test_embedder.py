import openai
import pytest

from app.core.exceptions import AIProviderError
from app.services.embedder import EMBEDDING_DIMENSIONS, MAX_BATCH_SIZE, generate_embeddings


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


def test_generate_embeddings_divide_em_lotes_de_ate_max_batch_size(monkeypatch):
    # Reproduz o bug real: o Gemini rejeita lotes com mais de 100 itens numa
    # única chamada (BatchEmbedContentsRequest) — aqui simulamos essa regra.
    from types import SimpleNamespace
    from app.services import embedder

    calls = []

    def fake_create(model, input, dimensions):
        calls.append(len(input))
        if len(input) > MAX_BATCH_SIZE:
            raise AssertionError("não deveria mandar mais que MAX_BATCH_SIZE por vez")
        return SimpleNamespace(data=[SimpleNamespace(embedding=[0.0]) for _ in input])

    monkeypatch.setattr(embedder.client.embeddings, "create", fake_create)

    textos = [f"texto {i}" for i in range(MAX_BATCH_SIZE + 10)]
    result = generate_embeddings(textos)

    assert len(result) == len(textos)
    assert calls == [MAX_BATCH_SIZE, 10]


def test_generate_embeddings_tenta_de_novo_apos_rate_limit_e_depois_funciona(monkeypatch):
    from types import SimpleNamespace
    from app.services import embedder


    attempts = {"n": 0}

    def fake_create(model, input, dimensions):
        attempts["n"] += 1
        if attempts["n"] == 1:
            raise openai.RateLimitError(
                message="limite excedido",
                response=_fake_response(429),
                body=None,
            )
        return SimpleNamespace(data=[SimpleNamespace(embedding=[0.0]) for _ in input])

    monkeypatch.setattr(embedder.client.embeddings, "create", fake_create)

    result = generate_embeddings(["texto único"])

    assert len(result) == 1
    assert attempts["n"] == 2  # falhou uma vez, tentou de novo e deu certo


def test_generate_embeddings_desiste_apos_esgotar_tentativas_de_rate_limit(monkeypatch):
    from app.services import embedder


    def fake_create(model, input, dimensions):
        raise openai.RateLimitError(
            message="limite excedido",
            response=_fake_response(429),
            body=None,
        )

    monkeypatch.setattr(embedder.client.embeddings, "create", fake_create)

    with pytest.raises(AIProviderError, match="Limite de requisições"):
        generate_embeddings(["texto único"])


def _fake_response(status_code):
    import httpx
    return httpx.Response(status_code, request=httpx.Request("POST", "https://example.com"))
