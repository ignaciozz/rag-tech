from app.services.chunker import chunk_text


def test_texto_curto_vira_um_unico_chunk():
    pages = [{"page_number": 1, "text": "Um texto curto sobre FastAPI."}]

    chunks = chunk_text(pages, chunk_size=500, overlap=75)

    assert len(chunks) == 1
    assert chunks[0]["chunk_index"] == 0
    assert chunks[0]["page_number"] == 1
    assert chunks[0]["content"] == "Um texto curto sobre FastAPI."


def test_texto_longo_gera_varios_chunks_com_indice_sequencial():
    texto_longo = "FastAPI é um framework web moderno. " * 100
    pages = [{"page_number": 1, "text": texto_longo}]

    chunks = chunk_text(pages, chunk_size=50, overlap=10)

    assert len(chunks) > 1
    indices = [c["chunk_index"] for c in chunks]
    assert indices == list(range(len(chunks)))


def test_overlap_repete_conteudo_entre_chunks_consecutivos():
    texto_longo = "palavra " * 200
    pages = [{"page_number": 1, "text": texto_longo}]

    chunks = chunk_text(pages, chunk_size=50, overlap=15)

    # Com overlap > 0, o fim de um chunk deve reaparecer no início do próximo.
    fim_chunk_0 = chunks[0]["content"][-20:]
    inicio_chunk_1 = chunks[1]["content"][:40]
    assert fim_chunk_0.strip().split()[-1] in inicio_chunk_1


def test_page_number_e_preservado_por_pagina():
    pages = [
        {"page_number": 1, "text": "Conteúdo da página um."},
        {"page_number": 2, "text": "Conteúdo da página dois."},
    ]

    chunks = chunk_text(pages, chunk_size=500, overlap=75)

    assert [c["page_number"] for c in chunks] == [1, 2]
    # chunk_index continua global (não reinicia por página).
    assert [c["chunk_index"] for c in chunks] == [0, 1]


def test_lista_de_paginas_vazia_retorna_lista_vazia():
    assert chunk_text([], chunk_size=500, overlap=75) == []
