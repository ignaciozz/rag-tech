from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.db.session import get_db, engine
from app.db.session import get_db, engine, Base
from app.db import models  # Importa os modelos para serem registrados no Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para ingestão de documentação técnica e busca semântica fundamentada (RAG).",
    version=settings.VERSION,
)

# Configuração de CORS para permitir requisições do Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db():
    """Garante que a extensão pgvector esteja ativada no banco ao inicializar."""
    """Garante que a extensão pgvector e as tabelas estejam criadas no banco ao inicializar."""
    try:
        with engine.connect() as connection:
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            connection.commit()
        # Cria as tabelas do banco de dados se não existirem
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"⚠️ Aviso ao verificar extensão pgvector: {e}")
        print(f"⚠️ Aviso ao inicializar banco de dados: {e}")

@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint básico para verificar se a API está de pé."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@app.get("/health/db", tags=["Health"])
def health_check_db(db: Session = Depends(get_db)):
    """
    Endpoint para testar a comunicação direta com o PostgreSQL
    e verificar se a extensão pgvector está ativa e funcional.
    """
    try:
        # Testa consulta simples
        result = db.execute(text("SELECT version();")).scalar()
        
        # Verifica se o pgvector está instalado e ativo
        vector_ext = db.execute(
            text("SELECT extversion FROM pg_extension WHERE extname = 'vector';")
        ).scalar()

        return {
            "status": "connected",
            "database": "PostgreSQL",
            "postgres_version": result,
            "pgvector_active": vector_ext is not None,
            "pgvector_version": vector_ext or "não instalado"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro ao conectar ao banco de dados: {str(e)}"
        )

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Bem-vindo à API do {settings.PROJECT_NAME}!",
        "docs_url": "/docs"
    }
