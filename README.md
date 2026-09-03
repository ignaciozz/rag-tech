# RAG Tech Docs

Assistente de documentação técnica baseado em IA, desenvolvido com **Retrieval-Augmented Generation (RAG)**.

O **RAG Tech Docs** é uma aplicação voltada para consulta e aprendizado acelerado a partir de documentações técnicas de tecnologias específicas (ex: FastAPI, PostgreSQL, Python), trazendo respostas fundamentadas (*grounded*), contextualizadas e com indicação exata das fontes.

---

## 🏗️ Arquitetura e Stack Tecnológica

- **Backend:** Python 3.11+, FastAPI, Pydantic, Uvicorn
- **AI & RAG:** OpenAI API (Embeddings & LLMs), LangChain / LlamaIndex ou pipeline customizado de RAG
- **Banco de Dados:** PostgreSQL + extensão `pgvector` (Local via Docker ou Supabase)
- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Infraestrutura:** Docker, Docker Compose

Para entender todos os detalhes de visão de produto, requisitos e roadmap, confira [docs/rag-tech.md](docs/rag-tech.md).

---

## 📁 Estrutura de Pastas

```text
rag-tech/
├── docs/                       # Documentações, diagramas e referências do projeto
├── backend/                    # Servidor Python (FastAPI, RAG Engine, DB)
│   ├── app/
│   │   ├── api/                # Rotas e endpoints da API
│   │   ├── core/               # Configurações gerais e variáveis de ambiente
│   │   ├── db/                 # Conexão e modelos do banco de dados
│   │   ├── schemas/            # Schemas de validação Pydantic
│   │   ├── services/           # Lógica de RAG, Embeddings e Processamento
│   │   └── main.py             # Ponto de entrada da aplicação
│   ├── migrations/             # Scripts de migração do banco de dados
│   ├── requirements.txt        # Dependências Python
│   └── Dockerfile
├── frontend/                   # Interface Web (Next.js + React + Tailwind)
├── docker-compose.yml          # Orquestração de containers (PostgreSQL + pgvector)
├── .env.example                # Template de variáveis de ambiente
└── README.md
```

---

## 🚀 Como Começar

### Pré-requisitos
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+ (para o frontend)

*(Instruções detalhadas de execução serão adicionadas conforme os módulos forem implementados)*

