import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    """
    Formato de retorno da API após o upload e processamento de um documento.
    """
    id: uuid.UUID
    title: str
    technology: str
    version: str | None
    file_type: str
    created_at: datetime
    chunks_count: int

    # Permite o Pydantic ler os campos direto de um objeto SQLAlchemy (Document),
    # em vez de exigir um dicionário.
    model_config = ConfigDict(from_attributes=True)


class EmbedResponse(BaseModel):
    """
    Formato de retorno após gerar os embeddings dos chunks de um documento.
    """
    document_id: uuid.UUID
    chunks_embedded: int
