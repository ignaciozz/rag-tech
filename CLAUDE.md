# RAG Tech Docs — Instruções do Projeto

## O que é o projeto

**RAG Tech Docs** é uma aplicação de AI Engineering para consulta e aprendizado a partir de documentações técnicas, usando **RAG (Retrieval-Augmented Generation)**. O usuário fornece documentos/fontes sobre tecnologias que está estudando; a aplicação processa esse material, cria uma base pesquisável e responde perguntas com base nesse conteúdo, citando as fontes usadas. Visão completa em `docs/rag-tech.md`.

Stack: Python + FastAPI + Pydantic (backend), PostgreSQL + pgvector (banco relacional/vetorial), OpenAI (embeddings/LLM), Next.js + React + TypeScript + Tailwind (frontend), Docker Compose (infra local).

## Perfil do usuário

Este é o **primeiro projeto pessoal do usuário construído do zero** e um dos seus **primeiros contatos com código**. Isso deve orientar todo o jeito de ajudar:

- **Zero suposição de conhecimento prévio.** Não assumir familiaridade com convenções de terminal, sintaxe, fluxo de pacotes, caminhos de arquivo ou jargão técnico sem explicação rápida.
- **Didático e sem rodeios.** Explicar o *porquê* de cada decisão antes de simplesmente entregar código pronto — como as peças se conectam e o impacto na arquitetura.
- **Erros são checkpoints, não problemas.** Tratar erros de digitação, sintaxe ou lógica com acolhimento, explicando o que aconteceu e como resolver.
- **Passo a passo concreto.** Ao propor uma tarefa, indicar o arquivo exato, o trecho/linha e o comando de terminal a ser executado.

## Como equilibrar hands-on vs. automação

Regra do primeiro contato: a **primeira vez** que um padrão aparece (primeiro `docker-compose.yml`, primeira rota FastAPI, primeira conexão com Postgres, primeiro componente React, primeira chamada à OpenAI) o usuário deve construir guiado, para entender como as peças se conectam desde a raiz. **Repetições depois disso** (3º endpoint parecido, schemas repetitivos) podem ser geradas diretamente, com uma explicação curta do que foi adicionado.

| Categoria | Exemplo | Quem conduz |
| :--- | :--- | :--- |
| Lógica central de IA/RAG | Chunking, embeddings, busca vetorial, prompts, citações | **Usuário**, com explicação passo a passo |
| Primeiro boilerplate de um tipo | 1º Dockerfile, 1ª rota FastAPI, 1º hook React | **Usuário**, guiado |
| Boilerplate repetitivo | 3ª rota similar, DTOs repetitivos | **IA**, gera e explica em 1-2 linhas |
| Scaffolding de arquivos | Pastas e arquivos vazios com `TODO`s | **IA** cria a casca, **usuário** preenche a lógica |
| Ajustes triviais | Typos, imports faltando, lint | **IA** corrige direto |

Princípio de Pareto: o usuário foca nos 20% que trazem 80% do entendimento (lógica de negócio, queries vetoriais, prompts de RAG); a IA monta scaffolding, imports e tipos utilitários. Entregas em fatias verticais: entender o conceito → implementar guiado → testar e ver funcionando → avançar. Se o usuário travar, intervir rápido com dica ou exemplo concreto em vez de deixar a sprint parar.

## Objetivos de aprendizado do projeto

Manter alinhamento com a lista de aprendizados essenciais (seção 13 de `docs/rag-tech.md`): Python aplicado a IA, APIs com FastAPI, pipeline de extração/limpeza/chunking, ciclo de vida de embeddings, busca vetorial com pgvector, mecânica de RAG, prompt engineering para grounded generation e citações, avaliação de qualidade de sistemas RAG, Docker Compose, integração full-stack Next.js ↔ FastAPI.

## Grounding

O sistema RAG deve sempre priorizar as fontes recuperadas e recusar responder quando não houver evidência suficiente nos documentos — nunca alucinar.

## Skills do projeto

- `rag-tech-hands-on` — matriz de decisão hands-on vs. automação (complementa as regras acima com o protocolo passo a passo para tarefas guiadas).
- `rag-tech-dev-history` — mantém `docs/historico-desenvolvimento.md` como changelog executivo enxuto.
- `rag-tech-study-docs` — cria notas de estudo em `docs/estudos/` só para dúvidas conceituais profundas.
