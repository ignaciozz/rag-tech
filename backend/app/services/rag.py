from typing import Any, Dict, List

from app.services.embedder import client

CHAT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """Você é um assistente que responde perguntas sobre documentação técnica.

Regras obrigatórias:
1. Responda APENAS com base no contexto fornecido abaixo. Nunca use conhecimento externo.
2. Toda afirmação da sua resposta deve citar a fonte usando o formato [Fonte N], referenciando os números do contexto.
3. Se o contexto não tiver informação suficiente para responder, diga claramente que não há evidência nas fontes disponíveis — não invente uma resposta.
"""


def build_context(chunks: List[Dict[str, Any]]) -> str:
    """
    Formata os chunks recuperados em blocos numerados e identificados,
    prontos para serem injetados no prompt do LLM.
    """
    blocks = []
    for i, chunk in enumerate(chunks, start=1):
        header = f"[Fonte {i} — {chunk['document_title']}, página {chunk['page_number']}]"
        blocks.append(f"{header}\n{chunk['content']}")

    return "\n\n".join(blocks)


def generate_answer(question: str, chunks: List[Dict[str, Any]]) -> str:
    """
    Monta o prompt fundamentado (contexto + pergunta) e chama o LLM para
    gerar uma resposta com citações, ou recusa caso não haja evidência.
    """
    if not chunks:
        return "Não encontrei nenhuma fonte relevante na base de conhecimento para responder essa pergunta."

    context = build_context(chunks)
    user_prompt = f"Contexto:\n{context}\n\nPergunta: {question}"

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message.content
