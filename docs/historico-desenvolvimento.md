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
- Átomos: `Button`, `IconButton`, `Badge`, `CloseButton`, `ThemeToggle` (ícone sol/lua), `ProgressBar`.
- Moléculas: `UserMessage`, `AssistantMessage` (parse de `[Fonte N]`), `ChatInput`, `ErrorBanner` (com "Tente novamente"), `ConfirmDialog`, `Dropzone`.
- Organismos: `AppHeader` (compartilhado, navegação opcional com interceptação de clique), `ChatMessageList`, `ChatWindow`, `UploadPanel`.
- Template: `ChatPageTemplate`.
- Convenções de interação documentadas em [.claude/skills/rag-tech-chat-ui/SKILL.md](../.claude/skills/rag-tech-chat-ui/SKILL.md).

### 4. Conexão com a API
- [frontend/lib/api.ts](../frontend/lib/api.ts): `askQuestion()`, `uploadDocument()`, `embedDocument()` chamam a API de verdade, com timeout de 30s (`AbortController`) pra nunca ficar pendurado indefinidamente se o backend cair no meio de uma requisição.
- `ChatWindow` com estado real (histórico em memória, loading, erro com "Tente novamente" reenviando só a última pergunta); modal de confirmação (`ConfirmDialog`) ao navegar pra fora do chat com conversa em andamento.

### 5. Tela de Upload (`/`, rota inicial)
- `UploadPanel`: fluxo central único — `Dropzone` (clicar/arrastar) → campo de tecnologia inline → `ProgressBar` em etapas reais (20% selecionado → 60% upload → 90% embedding → 100% concluído), sem animação falsa de bytes.
- Orquestra no frontend o que o backend expõe como 2 chamadas separadas: `uploadDocument()` seguido de `embedDocument()` automaticamente — e com retry por etapa (se só o embedding falhar, tenta de novo sem reenviar o arquivo).
- Rotas: `/` = Documentos (upload + gerenciamento), `/chat` = conversa.

### 6. Gerenciamento de Documentos
- Backend: `GET /api/v1/documents` (lista com contagem de chunks totais/processados via agregação SQL — `func.count()` ignora `NULL` automaticamente) e `DELETE /{id}` (cascata já cuidava dos chunks).
- Armazenamento do arquivo original: upload agora salva os bytes em `backend/uploads/<id>.<extensão>` (gitignorado); `GET /{id}/download` devolve com `Content-Disposition: attachment`; apagar o documento remove o arquivo também. Documentos cadastrados antes dessa mudança não têm arquivo em disco (404 esperado ao tentar baixar).
- Frontend: `UploadPanel` deixou de ter janela própria (virou só o conteúdo); `DocumentList` (nova) busca/lista/apaga com `ConfirmDialog`; `DocumentManager` junta os dois numa única janela com `AppHeader` (link "Chat" voltou ao cabeçalho). Título de cada item é um link de download.
- Dois bugs de CSS corrigidos: scroll da lista não funcionava (faltava `min-h-0` em dois níveis do flex — item flex não encolhe abaixo do conteúdo sem isso) e barra de scroll agora invisível (`.scrollbar-hide`, cross-browser).

---

## 📅 Qualidade: Tratamento de Erros & Testes Automatizados

### 1. Erros do Provedor de IA
- [backend/app/core/exceptions.py](../backend/app/core/exceptions.py): `AIProviderError` + `translate_openai_error()` — traduz exceções do SDK da OpenAI (`AuthenticationError`, `RateLimitError`, `NotFoundError`, `APIConnectionError`, `InternalServerError`, `BadRequestError`) em mensagens acionáveis.
- `embedder.py` e `rag.py` capturam `openai.APIError` e relançam como `AIProviderError`, sem acoplar os services ao FastAPI; os endpoints (`/embed`, `/chat`) traduzem isso para `502 Bad Gateway`, no lugar do `500` genérico de antes.
- **Validado com 3 cenários reais:** chave inválida, provedor sobrecarregado (`503` do Gemini capturado ao vivo durante o teste) e caminho feliz restaurado — sem regressão.

### 2. Suíte de Testes (`pytest`)
- [backend/tests/](../backend/tests/): banco de teste dedicado (`rag_tech_docs_test`, mesmo Postgres), truncado entre testes; `TestClient` do FastAPI com `get_db` sobrescrito; mocks do cliente de IA via fábricas de fixture (`mock_embeddings`, `mock_chat`) — zero chamada de rede real, suíte inteira roda em <1s.
- 33 testes: `chunker` (5), `extractor` (6), `embedder` (2), `rag` (3), API de documentos (14, incluindo listagem/exclusão/download), API de chat (3).
- Cobre inclusive o tratamento de erro do item acima, de ponta a ponta pela API.

---

### 🎯 Próximos Passos Imediatos:
1. Garantir ambiente pronto para open source (README, documentação, etc.) — o projeto é portfólio público no GitHub; maior retorno imediato (quem avalia lê o README antes de rodar o projeto).
2. Avaliação de qualidade das respostas do RAG.
3. UX e refinos finais.

### 📌 Backlog (prioridade baixa por ora):
- Dockerizar backend e frontend (hoje só o Postgres está no `docker-compose.yml`). Decisão registrada: adiado — maior esforço/risco do que ganho imediato pro portfólio; README e demo pesam mais pra quem avalia sem rodar o projeto local.
