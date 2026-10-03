---
name: rag-tech-frontend-design
description: >-
  Diretrizes de design visual para o frontend do RAG Tech Docs (Next.js +
  Tailwind): minimalista, sóbrio, sem "AI slop". Acionar ao criar ou revisar
  qualquer componente visual, página ou tela do frontend.
---

# RAG Tech Frontend: Design Visual

Produto: uma interface de chat sobre documentação técnica, com respostas fundamentadas e citações rastreáveis. O design deve comunicar **precisão e confiança**, não "mais um chatbot de IA genérico".

**Filosofia:** modelos de IA tendem a convergir pro visualmente mais comum/"estatisticamente seguro" (o tal AI slop). O antídoto aqui é **minimalismo deliberado**, não maximalismo — cada escolha (cor, fonte, espaçamento) deve ter uma razão específica pro produto, nunca ser só "o padrão que apareceu". Isso não significa adicionar textura, assimetria ou camadas visuais pra parecer "único" — significa a propósito de ser simples: cada elemento que sobra na tela precisa justificar sua existência.

---

## Evitar "AI Slop" (lista de bloqueio)

Nunca usar, a menos que explicitamente pedido:
- Cards idênticos com `border-radius` uniforme repetido em tudo.
- Sombras genéricas tipo `rgba(0,0,0,.1)` em tudo que for um "box".
- Gradientes como preenchimento visual decorativo (sem função).
- Eyebrows em CAPS LOCK, setas decorativas em links, pontos médios (`·`) como separador decorativo.
- Ícone de robô/sparkle (✨) genérico pra indicar "isso é IA".
- Paletas clichê de "produto de IA" (roxo/azul gradiente, preto + verde ácido).

## Paleta

Definir 4–6 cores **nomeadas**, com propósito claro — não usar paleta padrão de template:
- 1 cor de fundo, 1 de texto principal, 1 de texto secundário.
- 1 cor de destaque (usada com moderação — ex: só no botão de enviar pergunta, nunca espalhada pela tela).
- 1 cor reservada **só** para marcar citações/fontes (ex: um tom neutro de "nota de rodapé", não uma cor vibrante).

## Tipografia

- Máximo 2 famílias de fonte (ex: uma para UI, uma monoespaçada para trechos de código citados). Se usar duas, que sejam claramente distintas uma da outra.
- Texto de resposta do assistente: largura de linha confortável para leitura — por volta de 80 caracteres por linha (não a largura total da tela em desktop).
- Sem destacar palavras isoladas com cor/negrito dentro do corpo do texto — se algo merece destaque, é estrutural (título, citação), não decorativo.

## Layout do chat

- Mensagem do usuário: alinhada à direita, compacta.
- Resposta do assistente: largura maior, texto corrido, sem "balão" de chat (balões de chat genéricos são o "AI slop" mais comum).
- Citações (`[Fonte N]`) aparecem como **referências discretas e clicáveis** (ex: numeradas, estilo nota de rodapé/tooltip), nunca como card grande e colorido por fonte — a citação é metadado de apoio, não o protagonista visual da tela.
- Estado vazio (nenhuma conversa ainda): convida à ação com uma frase clara (ex: sugestão de pergunta sobre a tecnologia já cadastrada), não um ícone genérico de "comece a conversar".

## Grid e layout estrutural

- Usar um grid de colunas disciplinado (ex: `grid`/`flex` do Tailwind) — a estrutura deve ser consistente entre telas, não inventada tela a tela.
- Breakpoints padrão do Tailwind (`sm`/`md`/`lg`), mobile-first: desenhar primeiro pra tela estreita (chat em coluna única), depois adaptar pra desktop (ex: lista de documentos ganhando uma barra lateral).
- Bordas esquerdas de elementos alinhadas entre seções diferentes da mesma tela — nada de conteúdo "flutuando" fora do eixo vertical comum.
- Proporção entre sidebar (se houver, ex: lista de documentos) e área de conteúdo (chat) consistente em todos os tamanhos de tela — não recalcular a proporção breakpoint a breakpoint sem motivo.
- **Não** romper a grade de propósito pra parecer "único" (grids assimétricos, elementos sobrepostos com z-index, deslocamentos manuais) — isso é uma tática maximalista, incompatível com o minimalismo deste projeto.

## Espaçamento e hierarquia

- Um elemento visual de destaque por tela — não competir por atenção.
- Espaçamento consistente (escala de 4/8px do Tailwind), sem padding arbitrário tipo `pt-[13px]`.
- Decoração sem função (linhas, ícones, molduras) só se ela também carregar informação — senão, remover.

## Movimento

- Transições sutis (ex: fade do texto chegando, não "digitação letra por letra" exagerada) — só para dar feedback de que algo está acontecendo, nunca como "efeito bonito" gratuito.
- Respeitar `prefers-reduced-motion`.

## Acessibilidade (checar antes de considerar uma tela "pronta")

- Contraste de texto/fundo compatível com WCAG 2.1 nível AA (mínimo 4.5:1 para texto normal).
- Toda informação transmitida por cor (ex: cor da citação) também disponível por outro meio (ex: número `[Fonte N]`, não só uma cor de fundo diferente).
- Elementos interativos (botão de enviar, referências de citação) alcançáveis e operáveis por teclado, com foco visível.
- Imagens/ícones com texto alternativo quando carregam informação (não decorativos).

## Tom do conteúdo (textos da UI)

- Botões com verbo de ação claro: "Perguntar", "Enviar documento" — nunca "Submit" ou "Enviar" genérico sem contexto.
- Mensagens de erro explicam o problema real (ex: "Não encontramos evidência nas fontes para responder isso" é melhor que "Erro ao processar").
- Sem jargão de IA explicado em excesso na interface — o usuário final do produto não precisa saber o que é "RAG"; ele só precisa confiar na resposta e conseguir checar a fonte.
