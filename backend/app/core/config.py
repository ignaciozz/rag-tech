from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Caminho para o arquivo .env na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    """
    Configurações centralizadas da aplicação.
    Carrega automaticamente as variáveis do arquivo .env.
    """
    PROJECT_NAME: str = "RAG Tech Docs"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Provedor de IA (embeddings + chat) — compatível com o SDK da OpenAI.
    # Padrão: Gemini (tier gratuito). Pra usar a OpenAI de verdade, troque
    # AI_BASE_URL para None/vazio e ajuste os nomes de modelo no .env.
    AI_API_KEY: str = "sua_chave_aqui"
    AI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    EMBEDDING_MODEL: str = "gemini-embedding-001"
    CHAT_MODEL: str = "gemini-2.0-flash"

    # PostgreSQL / pgvector
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/rag_tech_docs"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE if ENV_FILE.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

