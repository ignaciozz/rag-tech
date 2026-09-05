# 📚 Dependências do Backend — Para que serve cada biblioteca?

> **Pergunta/Dúvida:** *"Quais dependências foram instaladas no `requirements.txt` e para que serve cada uma?"*

---

## 1. Visão Geral da Stack Backend

As dependências instaladas no nosso ambiente Python estão divididas em 5 camadas funcionais:

```text
┌───────────────────────────────────────────────┐
│ 1. Web & API: FastAPI, Uvicorn, Pydantic      │
├───────────────────────────────────────────────┤
│ 2. Banco & Vetores: SQLAlchemy, pgvector      │
├───────────────────────────────────────────────┤
│ 3. Inteligência Artificial: OpenAI SDK        │
├───────────────────────────────────────────────┤
│ 4. Processamento de Documentos: pypdf, docx   │
├───────────────────────────────────────────────┤
│ 5. Utilitários: python-dotenv, multipart      │
└───────────────────────────────────────────────┘
```

---

## 2. Detalhamento por Biblioteca

### 🌐 1. Web & API
- **`fastapi`**: Framework web assíncrono e de alto desempenho para construir APIs REST tipadas.
- **`uvicorn[standard]`**: Servidor ASGI leve e ultrarrápido que executa a aplicação FastAPI.
- **`pydantic` & `pydantic-settings`**: Validação de dados de entrada e leitura tipada de variáveis de ambiente (`.env`).

### 🗄️ 2. Banco de Dados & Vetores
- **`sqlalchemy`**: ORM (*Object Relational Mapper*) para gerenciar tabelas e consultas como classes Python.
- **`psycopg[binary]`**: Driver de comunicação de rede de baixo nível com o PostgreSQL 16.
- **`pgvector`**: Habilita o tipo de dado `Vector` e operadores de busca por similaridade de cosseno no SQLAlchemy.
- **`alembic`**: Controle de versão e migrações estruturais do banco de dados.

### 🤖 3. Inteligência Artificial & RAG
- **`openai`**: SDK oficial para chamadas às APIs de Embeddings (`text-embedding-3-small`) e LLM (`gpt-4o`).

### 📄 4. Processamento Documental
- **`pypdf`**: Leitura e extração de texto estruturado página por página de arquivos PDF.
- **`python-docx`**: Extração de texto de documentos Microsoft Word (`.docx`).

### 🛠️ 5. Utilitários
- **`python-dotenv`**: Carrega chaves e segredos do arquivo `.env` para o ambiente.
- **`python-multipart`**: Habilita o upload de arquivos binários via formulários HTTP.

---

## 3. Pontos-chave para fixar (Cheat Sheet)

- 📌 **`requirements.txt` é a receita:** Ele permite reproduzir o ambiente de desenvolvimento em qualquer máquina com um único comando `pip install -r requirements.txt`.
- 📌 **Isolamento de funções:** Cada biblioteca cuida de um elo da corrente, sem acoplamento excessivo.

