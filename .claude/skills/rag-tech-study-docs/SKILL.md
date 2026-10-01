---
name: rag-tech-study-docs
description: >-
  Cria e gerencia notas de estudo essenciais em docs/estudos/ com alto rigor de relevância.
  Só deve ser acionada para dúvidas conceituais profundas, fundamentos de arquitetura,
  engenharia de IA/RAG, banco vetorial ou padrões essenciais, evitando poluição de arquivos.
---

# Skill: Gerador de Documentação de Estudos (Alto Rigor)

Esta skill define as regras estritas para a criação e manutenção de notas de estudo em `docs/estudos/`.

---

## 🎯 Objetivo e Filtro de Relevância (Rigor Alto)

**NÃO criar documentos para dúvidas triviais, pontuais ou efêmeras** (como comandos de terminal rápidos, correções de sintaxe simples ou erros passageiros de digitação). Essas dúvidas devem ser respondidas apenas no chat.

### ✅ Critérios de Inclusão (Quando CRIAR um documento de estudo):
O tema precisa atender a pelo menos um dos seguintes pilares:
1. **Fundamentos de Arquitetura & Engenharia de Software** (ex: organização de pacotes, padrões em camadas, ciclo de vida de APIs).
2. **Engenharia de IA & RAG** (ex: embeddings, similaridade vetorial, chunking strategies, grounded generation, reranking).
3. **Banco de Dados & Vetores** (ex: pgvector, índices HNSW vs IVFFlat, modelagem relacional + vetorial).
4. **Conceitos Estruturais do Ecossistema** (ex: ambientes virtuais, drivers de banco, servidores ASGI vs WSGI).

> 💡 **Parâmetro de referência:** As notas existentes `01` a `06` em `docs/estudos/` são o modelo padrão de profundidade e pertinência.

---

## 📂 Diretrizes de Organização

- **Diretório:** `docs/estudos/`
- **Nomenclatura:** `[XX]-[tema-em-kebab-case].md` (ex: `07-sqlalchemy-e-orm-models.md`)
- **Evitar fragmentação:** Se a dúvida for um desdobramento direto de um tema já documentado, **atualize o documento existente** em vez de criar um novo.
- **Manter o índice:** Sempre atualizar a tabela de links em `docs/estudos/README.md` ao criar uma nova nota.

---

## 📝 Estrutura Padrão

```markdown
# 📚 [Título Objetivo do Conceito]

> **Pergunta/Dúvida:** [A dúvida central formulada de forma clara]

---

## 1. O que é? (Explicação Simples e Direta)
[Conceito acessível com analogia prática, sem rodeios]

---

## 2. Por que usamos e qual problema resolve?
[Contexto no mundo real e aplicação no RAG Tech Docs]

---

## 3. Como funciona na prática?
[Exemplo de código limpo, diagrama ou fluxo passo a passo]

---

## 4. Pontos-chave para fixar (Cheat Sheet)
- 📌 [Ponto 1]
- 📌 [Ponto 2]
- 📌 [Ponto 3]
```
