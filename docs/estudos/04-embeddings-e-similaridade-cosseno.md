# 📚 Embeddings, Espaço Vetorial e Similaridade Cosseno

> **Pergunta/Dúvida:** *"Como funciona a geração de embeddings e o cálculo de distância matemática no RAG?"*

---

## 1. O que é um Embedding?

Computadores não entendem o sentido das palavras diretamente; eles entendem **números**.

Um **Embedding** é a representação matemática do **significado (semântica)** de um texto na forma de uma lista de números decimais (um vetor com centenas ou milhares de dimensões).

### 🗺️ Analogia do "Mapa de Significados" (Espaço Vetorial 2D)

```text
  Y (Animais)
  ^
6 |       [Gato]
5 |    [Cachorro]
4 |
3 |
2 |
1 |                              [FastAPI] (Tecnologia)
0 └────────────────────────────────────────> X
  0   1   2   3   ...            90
```

- Textos com significados próximos ficam com coordenadas muito próximas no espaço vetorial.
- Textos com significados diferentes ficam distantes.
- Na prática, a OpenAI utiliza **1.536 dimensões** (`text-embedding-3-small`), capturando sutilezas profundas de contexto e linguagem.

---

## 2. Busca Semântica vs Busca por Palavra-chave

- **Busca Tradicional (`LIKE '%texto%'`):** Falha se o usuário usar sinônimos ou palavras diferentes das que estão no documento.
- **Busca Semântica (RAG):** Compara o **vetor da pergunta** com os **vetores dos documentos**, encontrando trechos equivalentes em significado mesmo que as palavras sejam completamente diferentes.

---

## 3. Como funciona a Similaridade Cosseno?

Em vez de comparar a distância física simples, calculamos o **cosseno do ângulo ($\theta$) entre os dois vetores**:

```text
      Vetor A (Pergunta: "Como autenticar usuário?")
       \
        \  Ângulo θ pequeno -> Cosseno próximo de 1.0 (Significados idênticos!)
         \ 
          ---- Vetor B (Documento: "Guia de Login com JWT e OAuth2")
```

- **Cosseno = 1 ($\theta = 0^\circ$):** Significados idênticos.
- **Cosseno = 0 ($\theta = 90^\circ$):** Assuntos sem relação.

No PostgreSQL com pgvector, o operador `<=>` calcula essa distância diretamente:

```sql
SELECT texto, 1 - (embedding <=> '[vetor_da_pergunta]') AS similaridade
FROM chunks
ORDER BY embedding <=> '[vetor_da_pergunta]'
LIMIT 3;
```

---

## 4. Pontos-chave para fixar (Cheat Sheet)

- 📌 **Pipeline de Consulta:** Pergunta → Embedding OpenAI → Busca Top-K no pgvector → Montagem de Contexto → LLM gera resposta fundamentada.
- 📌 **Grounded Generation:** O LLM só deve responder com base nos trechos recuperados pela busca semântica, evitando alucinações.

