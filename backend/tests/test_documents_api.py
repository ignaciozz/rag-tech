import openai

from app.core.exceptions import AIProviderError


def test_upload_processa_arquivo_txt_com_sucesso(client):
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("exemplo.txt", b"FastAPI usa type hints para validacao.", "text/plain")},
        data={"technology": "FastAPI", "version": "0.110.0"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "exemplo.txt"
    assert body["technology"] == "FastAPI"
    assert body["chunks_count"] == 1


def test_upload_rejeita_formato_nao_suportado(client):
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("virus.exe", b"dados", "application/octet-stream")},
        data={"technology": "FastAPI"},
    )

    assert response.status_code == 400


def test_upload_exige_technology(client):
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("exemplo.txt", b"conteudo", "text/plain")},
    )

    # Pydantic/FastAPI rejeita antes de chegar na nossa lógica: campo obrigatório ausente.
    assert response.status_code == 422


def test_embed_gera_e_salva_vetor_para_chunks_pendentes(client, mock_embeddings):
    mock_embeddings(dimensions=1536)

    upload = client.post(
        "/api/v1/documents/upload",
        files={"file": ("exemplo.txt", b"FastAPI usa type hints.", "text/plain")},
        data={"technology": "FastAPI"},
    )
    document_id = upload.json()["id"]

    response = client.post(f"/api/v1/documents/{document_id}/embed")

    assert response.status_code == 200
    assert response.json() == {"document_id": document_id, "chunks_embedded": 1}


def test_embed_404_quando_nao_ha_chunk_pendente(client):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.post(f"/api/v1/documents/{fake_id}/embed")

    assert response.status_code == 404


def test_embed_502_quando_provedor_de_ia_falha(client, monkeypatch):
    upload = client.post(
        "/api/v1/documents/upload",
        files={"file": ("exemplo.txt", b"conteudo qualquer", "text/plain")},
        data={"technology": "FastAPI"},
    )
    document_id = upload.json()["id"]

    from app.services import embedder

    def fake_create(model, input, dimensions):
        raise openai.RateLimitError(
            message="limite excedido",
            response=_fake_response(429),
            body=None,
        )

    monkeypatch.setattr(embedder.client.embeddings, "create", fake_create)

    response = client.post(f"/api/v1/documents/{document_id}/embed")

    assert response.status_code == 502
    assert "Limite de requisições" in response.json()["detail"]


def _fake_response(status_code):
    import httpx
    return httpx.Response(status_code, request=httpx.Request("POST", "https://example.com"))
