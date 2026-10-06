# 📜 Histórico de Desenvolvimento — RAG Tech Docs

Este documento registra a evolução, decisões de arquitetura e passos práticos executados no projeto.

---

## 📅 Fase 1: Fundação e Infraestrutura Inicial

### 1. Concepção e Planejamento
- Leitura e alinhamento com o documento mestre de requisitos e arquitetura ([docs/rag-tech.md](rag-tech.md)).
- Escopo do MVP definido: Ingestão de Documentos, Embeddings, Busca Vetorial com pgvector, RAG Grounded e Interface de Chat com Citações.
- Instruções permanentes do assistente centralizadas em [CLAUDE.md](../CLAUDE.md) (perfil do usuário, protocolo hands-on, objetivos de aprendizado); skills específicas em [.claude/skills/](../.claude/skills/) (`rag-tech-dev-history`, `rag-tech-study-docs`, `rag-tech-hands-on`, `rag-tech-frontend-design`, `rag-tech-chat-ui`).

### 2. Estrutura de Pastas e Arquitetura
- Arquitetura em Camadas (Layered Architecture) modular no backend: `api/`, `core/`, `db/`, `schemas/`, `services/`.
- Frontend em Next.js com Atomic Design: `components/{atoms,molecules,organisms,templates}/`.

### 3. Infraestrutura com Docker
- [docker-compose.yml](../docker-compose.yml) com imagem `pgvector/pgvector:pg16`, volume persistente `postgres_data` e healthcheck (`pg_isready`).
- Container `rag_tech_postgres` validado na porta 5432.

### 4. Ambiente Python e Conexão com o Banco
- Dependências via `.venv` a partir de [backend/requirements.txt](../backend/requirements.txt).
- Configurações centralizadas com `pydantic-settings` em [backend/app/core/config.py](../backend/app/core/config.py).
- Engine SQLAlchemy e injeção de dependência (`get_db`) em [backend/app/db/session.py](../backend/app/db/session.py).
- Extensão `pgvector` ativada e validada; rotas `/health` e `/health/db` em [backend/app/main.py](../backend/app/main.py).

---

## 📅 Fase 2: Processamento de Documentos & Ingestão

### 1. Modelagem Relacional & Vetorial
- [backend/app/db/models.py](../backend/app/db/models.py): `Document` (metadados do arquivo) e `DocumentChunk` (texto, `chunk_index`, `page_number`, `embedding Vector(1536)`, FK em cascata).

### 2. Extração de Texto
- [backend/app/services/extractor.py](../backend/app/services/extractor.py): extração para `.txt`/`.md` (decode UTF-8), `.pdf` (pypdf, por página) e `.docx` (python-docx), unificados no mesmo formato de saída `{page_number, text}`.

### 3. Chunking
- [backend/app/services/chunker.py](../backend/app/services/chunker.py): divisão por **tokens** (não caracteres) com `tiktoken` (encoding `cl100k_base`), `chunk_size=500`/`overlap=75`, preservando `page_number` de origem.

### 4. Endpoint de Upload
- [backend/app/schemas/document.py](../backend/app/schemas/document.py): `DocumentResponse`, `EmbedResponse`.
- [backend/app/api/endpoints/documents.py](../backend/app/api/endpoints/documents.py): `POST /api/v1/documents/upload` — extrai, chunka e persiste `Document` + `DocumentChunk` (embedding `NULL` nesta fase, por decisão de desacoplar upload da chamada à IA).
- **Validado:** upload real de `.txt`, documento e chunks confirmados no Postgres.

---

## 📅 Fase 3: Embeddings

### 1. Geração e Armazenamento
- [backend/app/services/embedder.py](../backend/app/services/embedder.py): `generate_embeddings()` em lote, `dimensions=1536` (compatível com a coluna `Vector(1536)`).
- `POST /api/v1/documents/{id}/embed` em [documents.py](../backend/app/api/endpoints/documents.py): busca chunks com `embedding IS NULL` e preenche o vetor.
- **Validado de ponta a ponta com o Gemini:** embedding real gerado e salvo com 1536 dimensões confirmadas via `vector_dims()` no Postgres.

---

## 📅 Fase 4: RAG (Retrieval-Augmented Generation)

### 1. Busca Semântica
- [backend/app/services/retriever.py](../backend/app/services/retriever.py): `retrieve_relevant_chunks()` — embedding da pergunta + busca Top-K por distância de cosseno (`cosine_distance` do pgvector), join com `Document` para título/tecnologia.

### 2. Geração Fundamentada (Grounded QA)
- [backend/app/services/rag.py](../backend/app/services/rag.py): `build_context()` formata os chunks como `[Fonte N — título, página X]`; `generate_answer()` monta o prompt fundamentado (regras: responder só com o contexto, citar `[Fonte N]`, recusar se não houver evidência) e chama o LLM com `temperature=0`.
- [backend/app/schemas/chat.py](../backend/app/schemas/chat.py) + `POST /api/v1/chat` em [backend/app/api/endpoints/chat.py](../backend/app/api/endpoints/chat.py).
- **Validado de ponta a ponta com o Gemini:** pergunta real → resposta fundamentada com citação `[Fonte 1]` correta.

### 3. Provedor de IA configurável
- [backend/app/core/config.py](../backend/app/core/config.py): `AI_API_KEY`/`AI_BASE_URL`/`EMBEDDING_MODEL`/`CHAT_MODEL` generalizados (compatíveis com o SDK da OpenAI) em vez de hardcoded — permite trocar de provedor só pelo `.env`, sem tocar em código.
- [.env.example](../.env.example) documenta duas opções lado a lado: **Gemini** (gratuito, sem cartão, padrão) e **OpenAI** (paga, comentada). Troca é manual — ver decisão registrada de não fazer fallback automático de embeddings (vetores de provedores diferentes não são comparáveis entre si; fallback automático só faria sentido para o chat, não para embeddings).

---

## 📅 Frontend: Design System & Interface de Chat

### 1. Scaffold Next.js
- `create-next-app` em [frontend/](../frontend/): TypeScript, Tailwind v4, App Router.

### 2. Design System
- Tokens em [frontend/app/globals.css](../frontend/app/globals.css): paleta preto/branco/laranja (`#ed461d` como acento mínimo), modo claro/escuro via `next-themes`, escala de raio (sm/md/lg/xl) e sombra `shadow-soft`, fonte Poppins.
- Diretrizes documentadas em [.claude/skills/rag-tech-frontend-design/SKILL.md](../.claude/skills/rag-tech-frontend-design/SKILL.md), incluindo notas de contraste WCAG AA (texto vs. ícone sobre o laranja) e exceções deliberadas registradas.
- Styleguide viva em `/styleguide` ([frontend/app/styleguide/page.tsx](../frontend/app/styleguide/page.tsx)), renderizando os componentes reais.

### 3. Componentes em Atomic Design
- Átomos: `Button`, `IconButton`, `Badge`, `CloseButton`, `ThemeToggle`.
- Moléculas: `UserMessage`, `AssistantMessage` (parse de `[Fonte N]`), `ChatInput`, `ErrorBanner`.
- Organismos: `ChatHeader`, `ChatMessageList`, `ChatWindow`.
- Template: `ChatPageTemplate`.
- Convenções de interação documentadas em [.claude/skills/rag-tech-chat-ui/SKILL.md](../.claude/skills/rag-tech-chat-ui/SKILL.md).

### 4. Conexão com a API
- [frontend/lib/api.ts](../frontend/lib/api.ts): `askQuestion()` chama `POST /api/v1/chat` de verdade.
- `ChatWindow` com estado real (histórico em memória, loading, erro com "Tente novamente" reenviando só a última pergunta).

---

### 🎯 Próximos Passos Imediatos:
1. UI de upload de documentos no frontend (hoje só existe via Swagger/curl).
2. Tratamento de erro específico no backend para falhas do provedor de IA (hoje cai em `500` genérico).
3. Testes automatizados (`pytest` no backend).
4. Avaliação de qualidade das respostas do RAG.
