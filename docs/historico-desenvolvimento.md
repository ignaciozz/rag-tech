# 📜 Histórico de Desenvolvimento — RAG Tech Docs

Este documento registra a evolução, decisões de arquitetura e passos práticos executados no projeto.

---

## 📅 Fase 1: Fundação e Infraestrutura Inicial

### 1. Concepção e Planejamento
- Leitura e alinhamento com o documento mestre de requisitos e arquitetura ([docs/rag-tech.md](rag-tech.md)).
- Definição do escopo do MVP focado em: Ingestão de Documentos, Embeddings, Busca Vetorial com pgvector, RAG Grounded e Interface de Chat com Citações.
- Criação da skill base do agente mentor ([.agents/skills/rag-tech-mentor/SKILL.md](../.agents/skills/rag-tech-mentor/SKILL.md)) para suporte didático e consultivo.

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
- Criação do arquivo [backend/requirements.txt](../backend/requirements.txt) contendo:
  - Framework Web: `fastapi`, `uvicorn`, `pydantic`, `pydantic-settings`
  - Banco e Vetores: `sqlalchemy`, `psycopg[binary]`, `pgvector`, `alembic`
  - Inteligência Artificial: `openai`
  - Processamento Documental: `pypdf`, `python-docx`
  - Utilitários: `python-dotenv`, `python-multipart`
- Criação e ativação do ambiente virtual isolado `.venv`.
- Instalação completa de todas as dependências com `pip install -r backend/requirements.txt`.

---

### 🎯 Próximos Passos Imediatos:
1. Criar o módulo de configuração centralizada em `backend/app/core/config.py` para carregar as variáveis de ambiente.
2. Criar a conexão com o banco de dados em `backend/app/db/session.py` utilizando SQLAlchemy.
3. Criar endpoint de teste de conexão no FastAPI e validar a extensão `pgvector`.

