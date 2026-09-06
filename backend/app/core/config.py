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

    # OpenAI API
    OPENAI_API_KEY: str = "sua_chave_openai_aqui"

    # PostgreSQL / pgvector
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/rag_tech_docs"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE if ENV_FILE.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

