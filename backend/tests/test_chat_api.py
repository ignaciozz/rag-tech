def test_chat_recusa_quando_nao_ha_documentos_na_base(client, mock_embeddings):
    mock_embeddings()  # a pergunta ainda precisa virar vetor pra buscar

    response = client.post("/api/v1/chat", json={"question": "o que é FastAPI?"})

    assert response.status_code == 200
    body = response.json()
    assert "Não encontrei nenhuma fonte relevante" in body["answer"]
    assert body["sources"] == []


def test_chat_responde_com_citacao_quando_ha_documento_relevante(
    client, mock_embeddings, mock_chat
):
    # Mesmo vetor pra tudo: como é o único chunk no banco, ele sempre "vence"
    # a busca por similaridade, não importa a pergunta.
    mock_embeddings(vector=[0.1] * 1536)
    mock_chat(answer_text="FastAPI é um framework web [Fonte 1].")

    upload = client.post(
        "/api/v1/documents/upload",
        files={"file": ("exemplo.txt", b"FastAPI e um framework web.", "text/plain")},
        data={"technology": "FastAPI"},
    )
    document_id = upload.json()["id"]
    client.post(f"/api/v1/documents/{document_id}/embed")

    response = client.post("/api/v1/chat", json={"question": "o que é FastAPI?"})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "FastAPI é um framework web [Fonte 1]."
    assert len(body["sources"]) == 1
    assert body["sources"][0]["document_title"] == "exemplo.txt"
    assert body["sources"][0]["technology"] == "FastAPI"


def test_chat_exige_campo_question(client):
    response = client.post("/api/v1/chat", json={})

    assert response.status_code == 422
