from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db import models  # noqa: F401 — registra os modelos no Base
from app.db.session import Base, get_db
from app.main import app
from app.services import embedder

# Banco separado do de desenvolvimento, só pra testes — nunca mistura dado real.
TEST_DATABASE_URL = settings.DATABASE_URL.rsplit("/", 1)[0] + "/rag_tech_docs_test"


@pytest.fixture(scope="session", autouse=True)
def _create_test_database():
    """
    Garante que o banco 'rag_tech_docs_test' existe. CREATE DATABASE não
    pode rodar dentro de uma transação — por isso o AUTOCOMMIT aqui.
    """
    admin_engine = create_engine(settings.DATABASE_URL, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'rag_tech_docs_test'")
        ).scalar()
        if not exists:
            conn.execute(text("CREATE DATABASE rag_tech_docs_test"))
    admin_engine.dispose()


@pytest.fixture(scope="session")
def test_engine(_create_test_database):
    engine = create_engine(TEST_DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    """Uma sessão nova por teste; limpa as tabelas ao final (schema fica)."""
    SessionLocal = sessionmaker(bind=test_engine)
    session = SessionLocal()
    yield session
    session.close()
    with test_engine.connect() as conn:
        conn.execute(text("TRUNCATE document_chunks, documents RESTART IDENTITY CASCADE"))
        conn.commit()


@pytest.fixture
def client(db_session):
    """
    TestClient do FastAPI com o banco trocado pelo de teste. Sem usar
    `with TestClient(app) as c`: isso dispararia o evento de startup da
    aplicação (que cria tabelas no banco de DESENVOLVIMENTO) — não queremos
    tocar no banco real durante os testes.
    """
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    test_client.close()
    app.dependency_overrides.clear()


@pytest.fixture
def mock_embeddings(monkeypatch):
    """
    Fábrica de mock: substitui a chamada real de embeddings por uma
    resposta falsa e determinística, sem rede nem custo de API.
    """
    def _install(vector=None, dimensions=1536):
        fake_vector = vector or [0.01] * dimensions

        def fake_create(model, input, dimensions):
            data = [SimpleNamespace(embedding=fake_vector) for _ in input]
            return SimpleNamespace(data=data)

        monkeypatch.setattr(embedder.client.embeddings, "create", fake_create)
        return fake_vector

    return _install


@pytest.fixture
def mock_chat(monkeypatch):
    """Fábrica de mock: substitui a chamada real de chat por um texto fixo."""
    def _install(answer_text="Resposta de teste [Fonte 1]."):
        def fake_create(model, messages, temperature):
            message = SimpleNamespace(content=answer_text)
            choice = SimpleNamespace(message=message)
            return SimpleNamespace(choices=[choice])

        monkeypatch.setattr(embedder.client.chat.completions, "create", fake_create)
        return answer_text

    return _install
