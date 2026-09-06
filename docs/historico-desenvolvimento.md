# 📜 Histórico de Desenvolvimento — RAG Tech Docs

Este documento registra a evolução, decisões de arquitetura e passos práticos executados no projeto.

---

## 📅 Fase 1: Fundação e Infraestrutura Inicial

### 1. Concepção e Planejamento
- Leitura e alinhamento com o documento mestre de requisitos e arquitetura ([docs/rag-tech.md](rag-tech.md)).
- Definição do escopo do MVP focado em: Ingestão de Documentos, Embeddings, Busca Vetorial com pgvector, RAG Grounded e Interface de Chat com Citações.
- Criação das skills do assistente em `.agents/skills/`:
  - `rag-tech-mentor`: Mentor didático para guiar desenvolvimento e aprendizado.
  - `rag-tech-study-docs`: Gerador de notas conceituais essenciais em `docs/estudos/`.
  - `rag-tech-dev-history`: Mantenedor conciso e estruturado deste histórico.

---

### 2. Estrutura de Pastas e Arquitetura do Projeto
Foi estabelecida uma **Arquitetura em Camadas (Layered Architecture)** modular:

```text
rag-tech/
├── .agents/                    # Configurações e skills do assistente Antigravity
├── docs/                       # Documentações, especificações e notas de estudo
│   ├── estudos/                # Pílulas conceituais e materiais de fixação
│   ├── historico-desenvolvimento.md
│   └── rag-tech.md
├── backend/                    # Servidor Python com FastAPI
│   ├── app/
│   │   ├── api/                # Endpoints HTTP da API
│   │   ├── core/               # Configurações globais e leitura do .env
│   │   ├── db/                 # Conexão e modelos do banco PostgreSQL/pgvector
│   │   ├── schemas/            # Contratos e validações Pydantic
│   │   ├── services/           # Regras de negócio (RAG, Embeddings, Ingestão)
│   │   └── main.py             # Ponto de entrada da aplicação
│   ├── migrations/             # Migrações do banco (Alembic)
│   └── requirements.txt        # Dependências Python
├── frontend/                   # Interface web com Next.js
├── docker-compose.yml          # Container do PostgreSQL 16 + pgvector
├── .env.example                # Template de variáveis de ambiente
├── .gitignore                  # Arquivos ignorados pelo Git
└── README.md                   # Apresentação do repositório
```

---

### 3. Infraestrutura de Banco de Dados com Docker
- Criação do [docker-compose.yml](../docker-compose.yml) utilizando a imagem oficial `pgvector/pgvector:pg16`.
- Configuração de volume persistente `postgres_data` para retenção dos dados.
- Mapeamento de porta `5432:5432` e healthcheck com `pg_isready`.
- Inicialização com sucesso via `docker compose up -d` (Container `rag_tech_postgres` ativo).

---

### 4. Configuração do Ambiente Python
- Criação do [backend/requirements.txt](../backend/requirements.txt) contendo FastAPI, SQLAlchemy, psycopg v3, pgvector, OpenAI, pypdf e utilitários.
- Criação e ativação do ambiente virtual isolado `.venv`.
- Instalação das dependências com `pip install -r backend/requirements.txt`.

---

### 5. Configurações Globais e Conexão com o Banco de Dados
- Implementação de [backend/app/core/config.py](../backend/app/core/config.py) utilizando `pydantic-settings` para carregamento seguro do `.env`.
- Implementação de [backend/app/db/session.py](../backend/app/db/session.py) gerenciando o `engine` SQLAlchemy e o gerador de sessões `get_db`.
- Atualização de [backend/app/main.py](../backend/app/main.py) com rotas `/health` e `/health/db`.
- **Validação:** Ativação e verificação da extensão `pgvector (v0.8.6)` no PostgreSQL com teste automatizado executado com sucesso.

---

### 🎯 Próximos Passos (Início da Fase 2 — Processamento de Documentos):
1. Modelagem das tabelas no banco de dados (`Document` e `DocumentChunk`) usando SQLAlchemy + pgvector.
2. Criação do serviço de extração e limpeza de texto (`app/services/document_service.py`) para PDF, DOCX, TXT e Markdown.
3. Criação da estratégia de *Chunking* (divisão em blocos de texto com sobreposição/overlap).
