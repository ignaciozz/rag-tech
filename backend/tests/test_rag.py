import pytest

from app.services.rag import build_context, generate_answer


def test_build_context_formata_blocos_numerados_com_fonte_e_pagina():
    chunks = [
        {"document_title": "FastAPI", "page_number": 3, "content": "Texto A"},
        {"document_title": "FastAPI", "page_number": 5, "content": "Texto B"},
    ]

    context = build_context(chunks)

    assert "[Fonte 1 — FastAPI, página 3]\nTexto A" in context
    assert "[Fonte 2 — FastAPI, página 5]\nTexto B" in context


def test_generate_answer_recusa_sem_chamar_llm_quando_nao_ha_chunks(monkeypatch):
    # Sem mock de propósito: se o código chamar o LLM aqui, queremos uma
    # falha imediata e clara — não uma tentativa real de rede.
    from app.services import embedder

    def fail_if_called(*args, **kwargs):
        pytest.fail("generate_answer não deveria chamar o LLM sem chunks")

    monkeypatch.setattr(embedder.client.chat.completions, "create", fail_if_called)

    answer = generate_answer("pergunta qualquer", [])

    assert "Não encontrei nenhuma fonte relevante" in answer


def test_generate_answer_retorna_texto_do_llm_quando_ha_chunks(mock_chat):
    texto_esperado = "O FastAPI é ótimo [Fonte 1]."
    mock_chat(answer_text=texto_esperado)
    chunks = [{"document_title": "FastAPI", "page_number": 1, "content": "..."}]

    answer = generate_answer("o que é FastAPI?", chunks)

    assert answer == texto_esperado
