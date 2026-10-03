---
name: rag-tech-chat-ui
description: >-
  Padrões técnicos para a interface de chat do RAG Tech Docs (envio de
  pergunta, estados de loading/erro, renderização de citações), adaptados
  ao endpoint real POST /api/v1/chat (resposta JSON completa, sem streaming
  ainda). Acionar ao implementar ou revisar a tela/componente de chat.
---

# RAG Tech Frontend: Padrões da Interface de Chat

## Contrato real com o backend

`POST /api/v1/chat` recebe `{ question: string }` e devolve, de uma vez (sem streaming):
```json
{ "answer": "...", "sources": [{ "document_title", "technology", "page_number" }] }
```
Isso muda o design da UI em relação a um chat "padrão de mercado": **não há token chegando aos poucos** — a resposta aparece completa quando a requisição termina. Não simular streaming falso (ex: revelar a resposta letra por letra depois de já ter ela inteira) — isso é teatro, não funcionalidade; é preferível um estado de loading honesto.

> Se decidirmos implementar streaming de verdade no futuro (backend com `StreamingResponse`/SSE), esta skill precisa ser revisada — o tratamento de estado abaixo mudaria.

## Estados da conversa

Cada pergunta enviada passa por 3 estados possíveis — a UI precisa representar os três, não só o "sucesso":

1. **Enviando/aguardando** — desabilitar o campo de envio, mostrar indicador de progresso (ex: os "..." discretos, não um spinner genérico de IA). A chamada pode demorar (busca vetorial + chamada ao LLM) — o usuário precisa perceber que está em andamento, não travado.
2. **Resposta recebida** — renderizar `answer` como texto corrido; renderizar cada item de `sources` como referência numerada (`[Fonte 1]` etc.) que, ao clicar/hover, mostra `document_title`, `technology` e `page_number`.
3. **Erro** — distinguir ao menos dois casos, com mensagens diferentes:
   - Erro de rede/servidor (ex: 500) → mensagem genérica de falha, com opção de tentar de novo.
   - Resposta de recusa por falta de evidência (o backend já devolve isso como texto normal em `answer`, não como erro HTTP — ver `rag.py:generate_answer`) → **não é um erro**, é tratado como resposta válida, só exibida sem citações.

## Persistência do histórico

- Guardar as mensagens da conversa no estado do componente (ex: lista de `{ role, content, sources? }`), não só a última pergunta/resposta — o usuário precisa poder rolar pra ver o que já perguntou.
- Cada mensagem do usuário e cada resposta do assistente tem identidade própria (ex: um id local, mesmo que gerado no cliente) para o React conseguir fazer `key` estável nas listas, sem usar o índice do array.
- Não é necessário (ainda) persistir a conversa no backend entre sessões — isso não existe na API hoje. Se o usuário recarregar a página, a conversa pode se perder; não fingir que persiste.

## Renderização de texto

- `answer` pode conter markdown leve (listas, negrito) se o modelo gerar — usar um renderer de markdown, não inserir `answer` como HTML bruto (evitar risco de XSS e também texto quebrado).
- As marcações `[Fonte N]` dentro do texto da resposta devem ser identificadas e transformadas em referências clicáveis — não deixar como texto literal "[Fonte 1]" solto no meio do parágrafo.

## Formulário de pergunta

- Envio tanto por botão quanto por Enter (sem Shift) — comportamento esperado de qualquer chat.
- Não permitir envio de pergunta vazia ou enquanto uma resposta anterior ainda está carregando (evita duas chamadas simultâneas disputando o mesmo estado de conversa).
