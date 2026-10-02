from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Pergunta enviada pelo usuário ao sistema de RAG."""
    question: str


class SourceInfo(BaseModel):
    """Uma fonte (chunk) usada para fundamentar a resposta."""
    document_title: str
    technology: str
    page_number: int | None


class ChatResponse(BaseModel):
    """Resposta fundamentada, com as fontes citadas."""
    answer: str
    sources: list[SourceInfo]
