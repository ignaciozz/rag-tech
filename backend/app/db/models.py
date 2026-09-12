import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.session import Base

class Document(Base):
    """
    Tabela que representa o Documento Pai (ex: PDF da documentação do FastAPI).
    """
    __tablename__ = "documents"

    # Identificador único (UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Nome do documento (ex: "FastAPI Tutorial")
    title = Column(String(255), nullable=False)
    
    # Tecnologia relacionada (ex: "FastAPI", "Python", "PostgreSQL")
    technology = Column(String(100), nullable=False, index=True)
    
    # Versão da tecnologia (ex: "0.110.0") - Opcional
    version = Column(String(50), nullable=True)
    
    # Tipo do arquivo original (ex: "pdf", "docx", "md", "txt")
    file_type = Column(String(20), nullable=False)
    
    # Data e hora do envio
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamento 1 para N: Um documento possui vários chunks (pedaços)
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    """
    Tabela que guarda os pedaços (chunks) de texto extraídos e seus vetores de IA.
    """
    __tablename__ = "document_chunks"

    # Identificador único do chunk
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Chave estrangeira que conecta este chunk ao Document pai
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)

    # Ordem sequencial do trecho dentro do documento
    chunk_index = Column(Integer, nullable=False)

    # Conteúdo textual do pedaço
    content = Column(Text, nullable=False)

    # Página de origem (para arquivos paginados como PDF)
    page_number = Column(Integer, nullable=True)

    # Vetor de embedding gerado pela OpenAI (1536 dimensões)
    embedding = Column(Vector(1536), nullable=True)

    # Data de criação
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamento inverso com o Document pai
    document = relationship("Document", back_populates="chunks")
