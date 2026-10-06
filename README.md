# RAG Tech Docs

Assistente de documentação técnica baseado em IA, desenvolvido com **Retrieval-Augmented Generation (RAG)**.

O **RAG Tech Docs** é uma aplicação voltada para consulta e aprendizado acelerado a partir de documentações técnicas de tecnologias específicas (ex: FastAPI, PostgreSQL, Python), trazendo respostas fundamentadas (*grounded*), contextualizadas e com indicação exata das fontes.

---

## 🏗️ Arquitetura e Stack Tecnológica

- **Backend:** Python 3.11+, FastAPI, Pydantic, SQLAlchemy, Uvicorn
- **AI & RAG:** pipeline de RAG customizado (extração → chunking → embeddings → busca vetorial → grounded QA), via SDK da OpenAI compatível com **Gemini** (gratuito) ou **OpenAI** — ver [.env.example](.env.example)
- **Banco de Dados:** PostgreSQL + extensão `pgvector` (local via Docker)
- **Frontend:** Next.js (App Router), React, TypeScript, Tailwind CSS v4, Atomic Design
- **Infraestrutura:** Docker, Docker Compose

Para entender todos os detalhes de visão de produto, requisitos e roadmap, confira [docs/rag-tech.md](docs/rag-tech.md).

---

## 📁 Estrutura de Pastas

```text
rag-tech/
├── docs/                       # Documentações, histórico e notas de estudo
├── .claude/skills/              # Skills do assistente (design, hands-on, histórico)
├── backend/                    # Servidor Python (FastAPI, RAG Engine, DB)
│   ├── app/
│   │   ├── api/endpoints/       # Rotas (documents, chat)
│   │   ├── core/                # Configurações e variáveis de ambiente
│   │   ├── db/                  # Conexão e modelos (Document, DocumentChunk)
│   │   ├── schemas/             # Contratos Pydantic
│   │   ├── services/            # extractor, chunker, embedder, retriever, rag
│   │   └── main.py
│   └── requirements.txt
├── frontend/                   # Next.js (App Router) + Atomic Design
│   ├── app/                     # Rotas: / (chat), /styleguide
│   ├── components/{atoms,molecules,organisms,templates}/
│   └── lib/                     # types.ts, api.ts
├── docker-compose.yml          # Container PostgreSQL + pgvector
├── .env.example                # Template de variáveis de ambiente
└── README.md
```

---

## 🚀 Como Começar

### Pré-requisitos
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+ (para o frontend)
- Uma chave de API gratuita do **Gemini** (https://aistudio.google.com/apikey) — ou uma chave paga da OpenAI, se preferir

### 1. Variáveis de ambiente
```bash
cp .env.example .env
# Edite .env e preencha AI_API_KEY (Gemini por padrão já vem configurado)
```

### 2. Banco de dados
```bash
docker compose up -d
```

### 3. Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```
API disponível em http://localhost:8000/docs (Swagger).

### 4. Frontend
```bash
cd frontend
npm install
npm run dev
```
Interface em http://localhost:3000 (chat) e http://localhost:3000/styleguide (Design System).

