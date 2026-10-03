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

## Como funciona o hands-on neste projeto

**Quem escreve o código é a IA.** O usuário não precisa digitar implementação na mão — a experiência hands-on vem de **acompanhar e entender tudo o que é feito**, não de ser quem produz as teclas. O objetivo é aprendizado real, nunca a sensação de "o código apareceu magicamente".

Isso muda o fluxo de toda implementação não-trivial (ou seja, tudo exceto ajustes triviais como typos/lint):

1. **Antes de codar** — explicar o objetivo, o conceito-chave novo (se houver) e a decisão técnica tomada, incluindo alternativas consideradas e por que esta foi escolhida.
2. **Implementar** — a IA escreve o código diretamente nos arquivos.
3. **Depois de codar** — caminhar pelo código escrito: o que cada parte faz, como se conecta ao resto do fluxo de dados/arquitetura, e qualquer trade-off relevante.
4. **Testar junto** — rodar o comando ou abrir o Swagger/navegador para ver a funcionalidade funcionando de fato.
5. **Abrir espaço para revisão** — convidar perguntas e aceitar questionamento das decisões antes de avançar para a próxima peça.

Princípio de Pareto aplicado à explicação (não à autoria): dedicar mais tempo explicando os 20% que trazem 80% do entendimento — lógica de negócio, queries vetoriais, prompts de RAG, decisões de arquitetura — e ser mais breve em boilerplate repetitivo (ex.: a 3ª rota parecida), sem deixar de mostrar o que foi feito.

## Objetivos de aprendizado do projeto

Manter alinhamento com a lista de aprendizados essenciais (seção 13 de `docs/rag-tech.md`): Python aplicado a IA, APIs com FastAPI, pipeline de extração/limpeza/chunking, ciclo de vida de embeddings, busca vetorial com pgvector, mecânica de RAG, prompt engineering para grounded generation e citações, avaliação de qualidade de sistemas RAG, Docker Compose, integração full-stack Next.js ↔ FastAPI.

## Grounding

O sistema RAG deve sempre priorizar as fontes recuperadas e recusar responder quando não houver evidência suficiente nos documentos — nunca alucinar.

## Skills do projeto

- `rag-tech-hands-on` — protocolo passo a passo (antes/durante/depois) para implementar de forma transparente e colaborativa.
- `rag-tech-dev-history` — mantém `docs/historico-desenvolvimento.md` como changelog executivo enxuto.
- `rag-tech-study-docs` — cria notas de estudo em `docs/estudos/` só para dúvidas conceituais profundas.
- `rag-tech-frontend-design` — diretrizes de design visual do frontend (minimalista, sem "AI slop").
- `rag-tech-chat-ui` — padrões técnicos da interface de chat, adaptados ao contrato real do `POST /api/v1/chat`.
