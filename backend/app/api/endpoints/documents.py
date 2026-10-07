import uuid
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AIProviderError
from app.db.models import Document, DocumentChunk
from app.db.session import get_db
from app.schemas.document import DocumentListItem, DocumentResponse, EmbedResponse
from app.services.chunker import chunk_text
from app.services.embedder import generate_embeddings
from app.services.extractor import extract_text

router = APIRouter()

SUPPORTED_EXTENSIONS = {"txt", "md", "pdf", "docx"}

FILE_MEDIA_TYPES = {
    "txt": "text/plain",
    "md": "text/markdown",
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def _file_path(document_id: uuid.UUID, file_type: str):
    """Caminho determinístico em disco: sempre <id>.<extensão>, nunca o nome original (evita colisão)."""
    return settings.UPLOADS_DIR / f"{document_id}.{file_type}"


@router.get("", response_model=List[DocumentListItem])
def list_documents(db: Session = Depends(get_db)):
    """
    Lista todos os documentos cadastrados, com a contagem de chunks totais
    e quantos já têm embedding — pra UI mostrar o status de processamento.
    """
    rows = (
        db.query(
            Document,
            func.count(DocumentChunk.id).label("total_chunks"),
            # func.count() ignora NULLs: conta só os chunks com embedding preenchido.
            func.count(DocumentChunk.embedding).label("embedded_chunks"),
        )
        .outerjoin(DocumentChunk, DocumentChunk.document_id == Document.id)
        .group_by(Document.id)
        .order_by(Document.created_at.desc())
        .all()
    )

    return [
        DocumentListItem(
            id=document.id,
            title=document.title,
            technology=document.technology,
            version=document.version,
            file_type=document.file_type,
            created_at=document.created_at,
            total_chunks=total_chunks,
            embedded_chunks=embedded_chunks,
        )
        for document, total_chunks, embedded_chunks in rows
    ]


@router.get("/{document_id}/download")
def download_document(document_id: uuid.UUID, db: Session = Depends(get_db)):
    """Devolve o arquivo original que foi enviado no upload."""
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado.",
        )

    path = _file_path(document.id, document.file_type)
    if not path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo original não encontrado em disco.",
        )

    return FileResponse(
        path,
        filename=document.title,
        media_type=FILE_MEDIA_TYPES.get(document.file_type, "application/octet-stream"),
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: uuid.UUID, db: Session = Depends(get_db)):
    """Apaga o documento, seus chunks em cascata e o arquivo original em disco."""
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado.",
        )

    path = _file_path(document.id, document.file_type)
    path.unlink(missing_ok=True)

    db.delete(document)
    db.commit()


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

    settings.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    _file_path(document.id, file_type).write_bytes(file_bytes)

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
    try:
        embeddings = generate_embeddings(texts)
    except AIProviderError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(error))

    for chunk, embedding in zip(chunks, embeddings):
        chunk.embedding = embedding

    db.commit()

    return EmbedResponse(document_id=document_id, chunks_embedded=len(chunks))
