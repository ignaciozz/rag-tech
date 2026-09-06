from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Criação do motor de conexão do SQLAlchemy
# pool_pre_ping=True verifica se a conexão ainda está viva antes de usá-la
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=(settings.ENVIRONMENT == "development")
)

# Fábrica de sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe Base para os futuros modelos ORM das tabelas
Base = declarative_base()

def get_db():
    """
    Função geradora de dependência (Dependency Injection) para o FastAPI.
    Abre uma sessão com o banco e garante seu fechamento após a requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

