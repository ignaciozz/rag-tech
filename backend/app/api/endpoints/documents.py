import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk
from app.db.session import get_db
from app.schemas.document import DocumentResponse, EmbedResponse
from app.services.chunker import chunk_text
from app.services.embedder import generate_embeddings
from app.services.extractor import extract_text

router = APIRouter()

SUPPORTED_EXTENSIONS = {"txt", "md", "pdf", "docx"}


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    technology: str = Form(...),
    version: str | None = Form(None),
    db: Session = Depends(get_db),
):
    """
    Recebe um arquivo de documentação técnica, extrai o texto, divide em
    chunks e persiste o documento + seus chunks no banco (embedding = NULL
    por enquanto; a geração do vetor acontece em uma etapa futura).
    """
    file_type = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""

    if file_type not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato não suportado: '{file_type}'. Use: {', '.join(SUPPORTED_EXTENSIONS)}.",
        )

    file_bytes = await file.read()
    pages = extract_text(file_bytes, file_type)
    chunks_data = chunk_text(pages)

    if not chunks_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível extrair nenhum texto do arquivo enviado.",
        )

    document = Document(
        title=file.filename,
        technology=technology,
        version=version,
        file_type=file_type,
    )
    db.add(document)
    db.flush()  # garante que document.id já exista, para usar como chave estrangeira abaixo

    for chunk_data in chunks_data:
        db.add(DocumentChunk(
            document_id=document.id,
            chunk_index=chunk_data["chunk_index"],
            page_number=chunk_data["page_number"],
            content=chunk_data["content"],
        ))

    db.commit()
    db.refresh(document)

    return DocumentResponse(
        id=document.id,
        title=document.title,
        technology=document.technology,
        version=document.version,
        file_type=document.file_type,
        created_at=document.created_at,
        chunks_count=len(chunks_data),
    )


@router.post("/{document_id}/embed", response_model=EmbedResponse)
def embed_document(document_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Gera e salva o embedding de todos os chunks do documento que ainda
    não têm vetor (embedding IS NULL).
    """
    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document_id, DocumentChunk.embedding.is_(None))
        .all()
    )

    if not chunks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum chunk pendente de embedding para este documento.",
        )

    texts = [chunk.content for chunk in chunks]
    embeddings = generate_embeddings(texts)

    for chunk, embedding in zip(chunks, embeddings):
        chunk.embedding = embedding

    db.commit()

    return EmbedResponse(document_id=document_id, chunks_embedded=len(chunks))
