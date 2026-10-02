from typing import List, Dict, Any
import tiktoken

# Mesmo encoding usado pelos modelos de embedding da OpenAI (text-embedding-3-small / ada-002)
ENCODING = tiktoken.get_encoding("cl100k_base")


def chunk_text(
    pages: List[Dict[str, Any]],
    chunk_size: int = 500,
    overlap: int = 75,
) -> List[Dict[str, Any]]:
    """
    Divide o texto de cada página (saída do extractor) em chunks de tamanho
    fixo em tokens, com sobreposição entre chunks consecutivos.
    """
    chunks: List[Dict[str, Any]] = []
    chunk_index = 0
    step = chunk_size - overlap

    for page in pages:
        tokens = ENCODING.encode(page["text"])

        for start in range(0, len(tokens), step):
            token_slice = tokens[start : start + chunk_size]
            text_piece = ENCODING.decode(token_slice).strip()

            if text_piece:
                chunks.append({
                    "chunk_index": chunk_index,
                    "page_number": page["page_number"],
                    "content": text_piece,
                })
                chunk_index += 1

    return chunks
