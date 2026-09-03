from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RAG Tech Docs API",
    description="API para ingestão de documentação técnica e busca semântica fundamentada (RAG).",
    version="0.1.0",
)

# Configuração básica de CORS para permitir requisições do Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint para verificar a saúde da API."""
    return {
        "status": "healthy",
        "service": "rag-tech-docs-api",
        "version": "0.1.0"
    }

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bem-vindo à API do RAG Tech Docs! Acesse /docs para ver a documentação interativa."}

