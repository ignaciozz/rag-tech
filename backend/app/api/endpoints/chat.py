from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse, SourceInfo
from app.services.rag import generate_answer
from app.services.retriever import retrieve_relevant_chunks

router = APIRouter()


@router.post("", response_model=ChatResponse)
def ask_question(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Pipeline de RAG completo: busca os chunks mais relevantes para a
    pergunta, monta o contexto e gera uma resposta fundamentada e citada.
    """
    chunks = retrieve_relevant_chunks(db, payload.question)
    answer = generate_answer(payload.question, chunks)

    sources = [
        SourceInfo(
            document_title=chunk["document_title"],
            technology=chunk["technology"],
            page_number=chunk["page_number"],
        )
        for chunk in chunks
    ]

    return ChatResponse(answer=answer, sources=sources)
