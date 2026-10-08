# RAG Tech Docs — Frontend

Interface em Next.js (App Router) para o [RAG Tech Docs](../README.md). Veja o README na raiz do projeto para visão geral, stack completa e como subir o backend/banco de dados.

## Rodando localmente

```bash
npm install
npm run dev
```

- **http://localhost:3000** — gerenciamento de documentos (upload, lista, download, exclusão)
- **http://localhost:3000/chat** — chat com citações
- **http://localhost:3000/styleguide** — Design System ao vivo (tokens, átomos, moléculas, organismos)

Requer o backend rodando em `http://localhost:8000` (ou ajuste `NEXT_PUBLIC_API_URL` num `.env.local`).

## Estrutura

Componentes organizados em **Atomic Design**:

```
components/
├── atoms/       # Button, IconButton, Badge, ProgressBar, ThemeToggle...
├── molecules/    # ChatInput, Dropzone, ConfirmDialog, DocumentListItem...
├── organisms/     # ChatWindow, DocumentManager, AppHeader...
└── templates/       # ChatPageTemplate
```

Tokens de design (cores, tipografia, raio, sombra) ficam em [`app/globals.css`](app/globals.css); o racional de cada decisão visual está documentado em [`.claude/skills/rag-tech-frontend-design/SKILL.md`](../.claude/skills/rag-tech-frontend-design/SKILL.md).
