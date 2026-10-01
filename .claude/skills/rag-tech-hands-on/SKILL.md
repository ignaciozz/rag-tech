---
name: rag-tech-hands-on
description: >-
  Protocolo passo a passo para propor e revisar uma tarefa de código hands-on
  (quando o usuário vai escrever o código guiado, não a IA). Acionar ao decidir,
  pela matriz do CLAUDE.md, que a tarefa atual é hands-on para o usuário.
---

# RAG Tech Hands-On: Protocolo de Tarefa Guiada

Pré-requisito: a decisão de "isso é hands-on ou automação" já foi tomada pela matriz em `CLAUDE.md`. Esta skill cobre **como conduzir** uma tarefa já classificada como hands-on.

---

## Passo 1: Instrução didática e direta

Ao propor a tarefa, entregar nesta ordem:

1. **O que vamos fazer** — objetivo em uma frase simples.
2. **Conceito-chave** — explicação rápida do conceito novo envolvido (ex.: "o que é um endpoint?", "o que significa `async`?").
3. **Onde fazer** — caminho completo do arquivo (ex.: `backend/app/api/endpoints/documents.py`).
4. **Esqueleto com `TODO`** — estrutura pronta (imports, assinatura de função/classe) com comentários indicando exatamente onde o usuário escreve a lógica.
5. **Dica amigável** — qual função/método usar, com um exemplo curto de sintaxe se ajudar.

## Passo 2: Code review educativo

Quando o usuário enviar o código escrito:

1. **Validar e celebrar** o que funcionou antes de apontar problemas.
2. **Explicar a causa** de qualquer erro ou melhoria de forma clara e construtiva — não só o "o quê", mas o "por quê".
3. **Testar na hora** — rodar o comando ou abrir o Swagger/navegador para ver a funcionalidade funcionando de fato.

## Anti-stall

Se o usuário travar em sintaxe ou erro, intervir imediatamente com um exemplo mastigado em vez de deixar a dúvida se arrastar — o objetivo é manter a tração sem pular a etapa de entendimento.

## Comunicação

- Comandos de terminal sempre completos e prontos para copiar (ex.: `docker compose up -d`), nunca descritos por extenso.
- Jargão (`middleware`, `payload`, `serialização`, `decorator`, etc.) sempre acompanhado de uma explicação breve na primeira vez que aparece na conversa.
