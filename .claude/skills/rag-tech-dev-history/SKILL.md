---
name: rag-tech-dev-history
description: >-
  Mantém e atualiza o arquivo docs/historico-desenvolvimento.md de forma concisa,
  rigorosa e estruturada. Registra apenas marcos relevantes e decisões de arquitetura,
  evitando prolixidade, redundâncias, crescimento descontrolado e gasto desnecessário de tokens.
---

# Skill: Gestão do Histórico de Desenvolvimento (Lean & Objective)

Esta skill define as diretrizes para alimentar e manter o documento `docs/historico-desenvolvimento.md` como um registro executivo, limpo e direto da evolução do projeto.

---

## 🎯 Princípios Fundamentais

1. **Rigor e Seletividade:** Registrar apenas **marcos concluídos (milestones)**, decisões de arquitetura e entregas de valor das fases do roadmap. 
   - ❌ **NÃO registrar:** Erros intermediários de digitação, comandos triviais de terminal ou testes descartáveis.
   - ✅ **SIM registrar:** Conclusão de infraestrutura, novos módulos arquiteturais, schemas criados, pipelines integrados e endpoints funcionais.

2. **Prevenção de Inchaço (Anti-Bloat & Token Efficiency):**
   - O documento deve ser um **sumário executivo**, não um diário minuto a minuto.
   - Manter o documento preferencialmente abaixo de **250 linhas**, condensando itens antigos se necessário.
   - Usar tópicos com *bullet points* diretos e links para os arquivos implementados.

3. **Check de Sanidade e Deduplicação Prévia:**
   - Antes de adicionar qualquer linha nova, leia o arquivo para verificar se a informação já não consta em outra seção.
   - Se uma funcionalidade foi apenas refinada ou corrigida, **atualize o item existente** em vez de criar um novo bloco.

---

## 📑 Estrutura Obrigatória do `historico-desenvolvimento.md`

O documento deve manter sempre esta organização enxuta:

```markdown
# 📜 Histórico de Desenvolvimento — RAG Tech Docs

Este documento registra a evolução, decisões de arquitetura e passos práticos executados no projeto.

---

## 📅 Fase [X]: [Nome da Fase Conforme Roadmap]

### 1. [Módulo / Marco Concluído]
- [Resumo conciso do que foi implementado e links de referência]
- [Decisão técnica tomada, se aplicável]

---

### 🎯 Próximos Passos Imediatos:
1. [Próxima tarefa imediata 1]
2. [Próxima tarefa imediata 2]
```

---

## 🔄 Checklist para Cada Atualização

- [ ] A mudança é um marco relevante e concluído?
- [ ] O texto é direto ao ponto, sem explicações redundantes?
- [ ] Foi verificado se a informação já existia no documento?
- [ ] A seção "Próximos Passos Imediatos" foi devidamente atualizada com o estado presente?

