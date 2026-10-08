import openai

from app.core.exceptions import AIProviderError


def test_list_vazio_quando_nao_ha_documentos(client):
    response = client.get("/api/v1/documents")

    assert response.status_code == 200
    assert response.json() == []


def test_list_mostra_status_de_embedding_correto(client, mock_embeddings):
    mock_embeddings()

    upload = client.post(
        "/api/v1/documents/upload",
        files={"file": ("exemplo.txt", b"FastAPI usa type hints.", "text/plain")},
        data={"technology": "FastAPI"},
    )
    document_id = upload.json()["id"]

    # Antes do /embed: 1 chunk total, 0 com embedding.
    antes = client.get("/api/v1/documents").json()
    assert antes[0]["total_chunks"] == 1
    assert antes[0]["embedded_chunks"] == 0

    client.post(f"/api/v1/documents/{document_id}/embed")

    depois = client.get("/api/v1/documents").json()
    assert depois[0]["embedded_chunks"] == 1


def test_list_ordena_do_mais_recente_para_o_mais_antigo(client):
    client.post(
        "/api/v1/documents/upload",
        files={"file": ("primeiro.txt", b"conteudo 1", "text/plain")},
        data={"technology": "A"},
    )
    client.post(
        "/api/v1/documents/upload",
        files={"file": ("segundo.txt", b"conteudo 2", "text/plain")},
        data={"technology": "B"},
    )

    titles = [doc["title"] for doc in client.get("/api/v1/documents").json()]

    assert titles == ["segundo.txt", "primeiro.txt"]


def test_delete_remove_documento_e_chunks_em_cascata(client):
    upload = client.post(
        "/api/v1/documents/upload",
        files={"file": ("exemplo.txt", b"conteudo", "text/plain")},
        data={"technology": "FastAPI"},
    )
    document_id = upload.json()["id"]

    response = client.delete(f"/api/v1/documents/{document_id}")

    assert response.status_code == 204
    assert client.get("/api/v1/documents").json() == []


def test_delete_404_quando_documento_nao_existe(client):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(f"/api/v1/documents/{fake_id}")

    assert response.status_code == 404


def test_download_devolve_o_arquivo_original_salvo_no_upload(client):
    conteudo_original = b"FastAPI usa type hints para validacao."
    upload = client.post(
        "/api/v1/documents/upload",
        files={"file": ("exemplo.txt", conteudo_original, "text/plain")},
        data={"technology": "FastAPI"},
    )
    document_id = upload.json()["id"]

    response = client.get(f"/api/v1/documents/{document_id}/download")

    assert response.status_code == 200
    assert response.content == conteudo_original
    assert "attachment" in response.headers["content-disposition"]
    assert "exemplo.txt" in response.headers["content-disposition"]


def test_download_404_quando_documento_nao_existe(client):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/api/v1/documents/{fake_id}/download")

    assert response.status_code == 404


def test_delete_remove_tambem_o_arquivo_do_disco(client):
    upload = client.post(
        "/api/v1/documents/upload",
        files={"file": ("exemplo.txt", b"conteudo", "text/plain")},
        data={"technology": "FastAPI"},
    )
    document_id = upload.json()["id"]

    client.delete(f"/api/v1/documents/{document_id}")

    # Sem o registro no banco, o download deve dar 404 — não achar o arquivo órfão.
    response = client.get(f"/api/v1/documents/{document_id}/download")
    assert response.status_code == 404


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
