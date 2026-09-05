# 📚 O que é o pgvector e Bancos de Dados Vetoriais?

> **Pergunta/Dúvida:** *"O pgvector surgiu depois da inteligência artificial? O foco dele é vetorização? O que ele é? Um framework?"*

---

## 1. O que é o `pgvector`?

**O `pgvector` NÃO é um framework.** Ele é uma **extensão (plugin) de código aberto para o banco de dados PostgreSQL**.

Pense no PostgreSQL tradicional como um carro muito confiável que sabe lidar com textos, números e datas. O **pgvector** adiciona um "turbo": ele introduz o tipo de dado `vector` e funções matemáticas ultrarrápidas para comparar vetores de alta dimensão diretamente em SQL.

---

## 2. Ele surgiu depois da Inteligência Artificial?

- **Conceito:** Vetores e álgebra linear existem na matemática e computação há décadas (usados em sistemas de recomendação de filmes, músicas, etc.).
- **Lançamento do pgvector:** Foi criado em **2021** (por Andrew Kane).
- **Boom de popularidade:** Explodiu a partir de **2023** com o surgimento do ChatGPT e das arquiteturas RAG.

**O problema que ele resolveu:**  
As empresas já utilizavam PostgreSQL para seus sistemas. Em vez de terem que contratar e aprender a operar um banco de dados novo exclusivo para vetores (como Pinecone, Qdrant, Chroma), o pgvector permitiu armazenar dados relacionais convencionais e vetores de IA no **mesmo banco de dados**.

---

## 3. O foco dele é vetorização?

**Não. O foco dele é ARMAZENAR e PESQUISAR vetores.**

- **Quem faz a vetorização (cria os números a partir do texto):** O modelo de IA (ex: API de Embeddings da OpenAI).
- **Quem guarda e faz a busca por similaridade:** O **pgvector** dentro do PostgreSQL.

```text
[Texto do Documento] ──(API da OpenAI)──> [Vetor: 0.012, -0.045, ...] ──(Salva)──> [PostgreSQL + pgvector]
```

---

## 4. Pontos-chave para fixar (Cheat Sheet)

- 📌 **Extensão, não framework:** Adiciona o tipo de dado `VECTOR(dimensoes)` ao PostgreSQL.
- 📌 **Busca híbrida:** Permite combinar filtros tradicionais (`WHERE tecnologia = 'FastAPI'`) com busca semântica vetorial na mesma consulta SQL.
- 📌 **Eficiência:** Suporta índices vetoriais avançados (HNSW e IVFFlat) para consultar milhões de trechos em milissegundos.

