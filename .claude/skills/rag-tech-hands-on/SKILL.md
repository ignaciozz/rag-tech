---
name: rag-tech-hands-on
description: >-
  Protocolo passo a passo para implementar código de forma transparente e
  colaborativa: a IA escreve, mas explica antes, caminha pelo código depois e
  convida revisão. Acionar em qualquer implementação não-trivial no projeto
  (ou seja, tudo exceto ajustes triviais como typo/lint).
---

# RAG Tech Hands-On: Implementação Transparente

A IA é quem escreve o código. O "hands-on" aqui é sobre o usuário **entender e acompanhar** cada decisão — não sobre digitar a implementação na mão. Ver `CLAUDE.md` para o racional completo.

---

## Passo 1: Antes de codar

1. **O que vamos fazer** — objetivo em uma frase simples.
2. **Conceito-chave** — explicação rápida de qualquer conceito novo envolvido (ex.: "o que é um endpoint?", "o que significa `async`?").
3. **Decisão técnica** — se havia mais de um caminho possível, dizer qual foi escolhido e por quê (mesmo que brevemente).

## Passo 2: Implementar

Escrever o código diretamente nos arquivos do projeto.

## Passo 3: Depois de codar

1. **Caminhar pelo código** — explicar o que cada parte faz e como se conecta ao resto do fluxo de dados/arquitetura.
2. **Testar na hora** — rodar o comando ou abrir o Swagger/navegador para confirmar que funciona de fato.
3. **Abrir espaço pra revisão** — convidar perguntas e aceitar questionamento das decisões antes de seguir para a próxima peça.

## Nível de detalhe

Mais explicação nos 20% que trazem 80% do entendimento (lógica de negócio, queries vetoriais, prompts de RAG, decisões de arquitetura); mais breve em boilerplate repetitivo (ex.: a 3ª rota parecida com a anterior) — mas sempre mostrando o que foi feito, nunca pulando a etapa de explicar.

## Comunicação

- Comandos de terminal sempre completos e prontos para copiar (ex.: `docker compose up -d`), nunca descritos por extenso.
- Jargão (`middleware`, `payload`, `serialização`, `decorator`, etc.) sempre acompanhado de uma explicação breve na primeira vez que aparece na conversa.
