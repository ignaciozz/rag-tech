# RAG Tech Docs

Assistente de documentação técnica com IA, construído do zero com **RAG (Retrieval-Augmented Generation)**: você envia documentações técnicas (PDF, DOCX, TXT, Markdown), a aplicação as transforma em uma base pesquisável, e você conversa com elas — recebendo respostas **fundamentadas**, com citação exata da fonte e da página de onde a informação veio.

Sem citação, sem resposta: o sistema é instruído a recusar quando não há evidência suficiente nos documentos, em vez de inventar.

---

## ✨ Funcionalidades

- **Upload multi-formato** — `.pdf`, `.docx`, `.txt`, `.md`, com extração de texto e divisão em chunks por token (não por caractere).
- **Busca semântica** — embeddings vetoriais armazenados no PostgreSQL com `pgvector`, recuperação por similaridade de cosseno.
- **Chat com citações rastreáveis** — cada resposta referencia `[Fonte N]`, ligada ao documento e à página de origem.
- **Gerenciamento de documentos** — listar, baixar o arquivo original e apagar (com confirmação), tudo pela interface.
- **Provedor de IA configurável** — funciona com o **Gemini** (tier gratuito, sem cartão) ou a **OpenAI**, trocando só uma variável de ambiente, sem mudar código.

## 🏗️ Stack

- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
- **IA & RAG:** pipeline próprio (extração → chunking → embeddings → busca vetorial → geração fundamentada), via SDK da OpenAI — compatível com Gemini ou OpenAI
- **Banco de dados:** PostgreSQL + `pgvector`
- **Frontend:** Next.js (App Router), React, TypeScript, Tailwind CSS v4 — componentes organizados em Atomic Design
- **Testes:** `pytest`, com banco de teste dedicado e mocks do provedor de IA (suíte roda sem rede, em menos de 2s)

> Só o PostgreSQL roda em Docker por enquanto — backend e frontend ainda rodam localmente (ver [Como começar](#-como-começar)). Dockerizar os dois está no roadmap.

## 🔄 Como funciona o pipeline de RAG

```
upload do arquivo
  → extração de texto (por página, quando aplicável)
  → chunking por token, com sobreposição entre blocos
  → embedding de cada chunk (vetor armazenado no Postgres)

pergunta do usuário
  → embedding da pergunta
  → busca por similaridade de cosseno (top-K chunks mais relevantes)
  → contexto montado com as fontes numeradas
  → LLM gera a resposta só com base nesse contexto, citando [Fonte N]
```

---

## 📁 Estrutura de Pastas

```text
rag-tech/
├── docs/                         # Documentação, histórico de desenvolvimento, notas de estudo
├── backend/
│   ├── app/
│   │   ├── api/endpoints/         # Rotas: documents (upload/listar/baixar/apagar/embed), chat
│   │   ├── core/                  # Configurações, variáveis de ambiente, tratamento de erros
│   │   ├── db/                    # Modelos (Document, DocumentChunk) e conexão
│   │   ├── schemas/                # Contratos Pydantic
│   │   ├── services/                # extractor, chunker, embedder, retriever, rag
│   │   └── main.py
│   ├── tests/                     # Suíte pytest (unitários + integração via TestClient)
│   └── requirements.txt
├── frontend/
│   ├── app/                       # Rotas: / (documentos), /chat, /styleguide
│   ├── components/{atoms,molecules,organisms,templates}/   # Atomic Design
│   └── lib/                       # Tipos e cliente de API
├── docker-compose.yml             # Container do PostgreSQL + pgvector
└── .env.example                   # Template de variáveis de ambiente
```

---

## 🚀 Como Começar

### Pré-requisitos
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- Uma chave de API gratuita do **Gemini** ([aistudio.google.com/apikey](https://aistudio.google.com/apikey)) — ou uma chave da OpenAI, se preferir

### 1. Variáveis de ambiente
```bash
cp .env.example .env
# Edite .env e preencha AI_API_KEY (o Gemini já vem pré-configurado como padrão)
```

### 2. Banco de dados
```bash
docker compose up -d
```

### 3. Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows — no Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```
API em http://localhost:8000/docs (Swagger).

### 4. Frontend
```bash
cd frontend
npm install
npm run dev
```
Interface em http://localhost:3000 — suba um documento, depois vá para `/chat` e pergunte sobre ele.

### 5. Rodando os testes (backend)
```bash
cd backend
pytest
```
A suíte usa um banco de teste separado (criado automaticamente) e mocks do provedor de IA — não precisa de chave de API nem conexão de rede pra rodar.

---

## 📖 Mais detalhes

- [docs/rag-tech.md](docs/rag-tech.md) — visão de produto, problema e requisitos completos.
- [docs/historico-desenvolvimento.md](docs/historico-desenvolvimento.md) — decisões de arquitetura e evolução do projeto, fase por fase.
- [docs/estudos/](docs/estudos/) — notas de estudo sobre os conceitos usados (pgvector, embeddings, chunking, etc.).
