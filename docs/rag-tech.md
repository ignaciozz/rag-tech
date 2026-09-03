# RAG Tech Docs

_Assistente de documentação técnica baseado em IA, desenvolvido com Retrieval-Augmented Generation (RAG)._

## 1. Visão do Projeto

O **RAG Tech Docs** é uma aplicação de AI Engineering voltada para consulta e aprendizado a partir de **documentações técnicas**.

O usuário fornece documentações, arquivos ou conteúdos relacionados às tecnologias que está estudando. A aplicação processa esse material, cria uma base de conhecimento pesquisável e permite fazer perguntas sobre o conteúdo utilizando **RAG (Retrieval-Augmented Generation)**.

O objetivo é criar uma camada especializada entre o desenvolvedor e a documentação técnica, permitindo consultar, compreender e explorar conteúdos de forma contextualizada.

A IA deve priorizar as informações presentes nas fontes fornecidas e indicar as referências utilizadas nas respostas.

---

## 2. Problema

Documentações técnicas são frequentemente extensas, fragmentadas e difíceis de consultar durante o aprendizado.

O estudante precisa alternar constantemente entre:

- documentação oficial;
- tutoriais;
- PDFs;
- anotações;
- exemplos;
- mecanismos de busca;
- ferramentas de IA.

Além disso, respostas genéricas de LLMs podem utilizar conhecimento desatualizado ou apresentar informações que não correspondem à documentação da tecnologia ou versão estudada.

O RAG Tech Docs busca resolver isso criando uma interface única para **consultar e compreender um conjunto específico de documentações**.

---

## 3. Proposta

Permitir que o usuário monte uma base de conhecimento técnica e converse com ela.

Exemplo:

O usuário adiciona a documentação do **FastAPI**.

Depois pergunta:

> "Como funciona Dependency Injection no FastAPI?"

O sistema:

1. transforma a pergunta em embedding;
2. busca os trechos mais relevantes da documentação;
3. fornece esses trechos ao LLM;
4. gera uma resposta baseada no contexto recuperado;
5. apresenta as fontes utilizadas.

Caso a informação não esteja disponível na base, a aplicação deve informar que não encontrou evidências suficientes para responder.

---

## 4. Público-alvo

Principalmente:

- estudantes de programação;
- desenvolvedores iniciantes;
- desenvolvedores que estão aprendendo novas tecnologias;
- pessoas estudando frameworks e bibliotecas;
- desenvolvedores que precisam consultar documentação frequentemente.

---

## 5. Funcionalidades do MVP

### 5.1. Gerenciamento de fontes

Permitir adicionar materiais à base de conhecimento.

Formatos iniciais:

- PDF;
- TXT;
- Markdown;
- DOCX.

Cada fonte deverá possuir informações como:

- nome;
- tipo;
- data de adição;
- tecnologia;
- versão, quando aplicável.

### 5.2. Processamento de documentos

Pipeline responsável por:

`Upload → Extração → Limpeza → Chunking → Embeddings → Armazenamento`

Os documentos serão divididos em pequenos trechos para permitir recuperação semântica eficiente.

### 5.3. Busca semântica

A pergunta do usuário será transformada em embedding.

O sistema utilizará busca vetorial para recuperar os trechos semanticamente mais relevantes.

### 5.4. Chat com a documentação

Interface de conversa para realizar perguntas sobre as fontes adicionadas.

Exemplos:

> "O que é Depends?"

> "Como criar um endpoint POST?"

> "Como funciona validação com Pydantic?"

> "Qual a diferença entre esses dois métodos?"

### 5.5. Respostas fundamentadas

As respostas devem ser baseadas prioritariamente nos documentos recuperados.

A aplicação deve evitar apresentar informações não encontradas nas fontes como fatos.

Quando possível, deve indicar:

- documento;
- seção;
- trecho utilizado;
- referência/origem.

### 5.6. Contexto por tecnologia

O usuário poderá organizar suas fontes por tecnologia.

Exemplo:

```
Python
 ├── Python Documentation
 ├── PEPs
 └── Minhas anotações

FastAPI
 ├── FastAPI Documentation
 └── FastAPI Tutorial

PostgreSQL
 └── PostgreSQL Documentation
```

---

## 6. Funcionalidades futuras

O MVP deve permanecer focado em consulta documental. Funcionalidades educacionais podem ser adicionadas posteriormente.

### Study Mode

Transformar a documentação em material de estudo:

- perguntas;
- quizzes;
- flashcards;
- exercícios;
- revisão de conceitos.

### Explain Mode

Permitir selecionar um trecho da documentação e solicitar uma explicação adaptada ao nível do usuário.

Exemplo:

> "Explique esse trecho como se eu estivesse começando a estudar FastAPI."

### Code Assistant

Utilizar a documentação como base para:

- explicar código;
- sugerir implementações;
- analisar erros;
- explicar APIs;
- criar pequenos exemplos.

### Learning Assistant

Criar uma camada de orientação:

> "O que devo estudar depois?"

> "Quais conceitos preciso dominar antes de aprender FastAPI?"

> "Quais assuntos aparecem com mais frequência nas minhas dúvidas?"

### Histórico de conhecimento

Registrar:

- perguntas;
- tecnologias consultadas;
- assuntos recorrentes;
- documentos mais utilizados.

### Avaliação da qualidade do RAG

Criar uma área para avaliar:

- relevância dos documentos recuperados;
- qualidade das respostas;
- precisão das citações;
- taxa de respostas sem evidência suficiente.

---

## 7. Arquitetura

Arquitetura inicial:

```
                    ┌──────────────────┐
                    │     Frontend     │
                    │ Next.js + TS     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      FastAPI     │
                    │     Backend      │
                    └────────┬─────────┘
                             │
                 ┌────────────┴────────────┐
                 ▼                         ▼
        ┌─────────────────┐       ┌─────────────────┐
        │ Document Engine │       │   RAG Engine     │
        └────────┬────────┘       └────────┬────────┘
                 │                         │
                 ▼                         ▼
        ┌─────────────────┐       ┌─────────────────┐
        │ Text Extraction │       │ Embeddings      │
        │ + Chunking      │       │ + Retrieval     │
        └────────┬────────┘       └────────┬────────┘
                 │                         │
                 └────────────┬────────────┘
                              ▼
                     ┌──────────────────┐
                     │   PostgreSQL     │
                     │    + pgvector    │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │       LLM        │
                     │  OpenAI API      │
                     └──────────────────┘
```

---

## 8. Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

- Python
- FastAPI
- Pydantic

### AI

- OpenAI API
- Embeddings
- LLM
- RAG

### Banco de dados

- PostgreSQL
- pgvector

### Processamento

Dependendo do formato:

- PyMuPDF/pdfplumber para PDF;
- python-docx para DOCX;
- processamento nativo para TXT/Markdown.

### Infraestrutura

Inicialmente:

- Docker;
- Docker Compose;
- `.env` para configurações e API keys.

---

## 9. Pipeline RAG

O núcleo técnico do projeto será:

```
                INGESTÃO

Documento
   ↓
Extração de texto
   ↓
Limpeza
   ↓
Chunking
   ↓
Embedding
   ↓
PostgreSQL + pgvector
```

E para consultas:

```
                QUERY

Pergunta do usuário
        ↓
      Embedding
        ↓
Busca vetorial
        ↓
Top-K chunks
        ↓
Construção do contexto
        ↓
       LLM
        ↓
Resposta fundamentada
        ↓
     Citações
```

Uma possível evolução será adicionar **reranking** entre a busca vetorial e a geração da resposta.

---

## 10. Princípio de Grounded Question Answering

O sistema deve funcionar como um mecanismo de **question answering grounded**.

Ou seja, a IA deve responder utilizando as evidências recuperadas das fontes disponíveis.

Regra principal:

> Se não houver evidência suficiente na base de conhecimento, o sistema deve deixar isso explícito.

Isso reduz o risco de respostas inventadas e permite demonstrar uma característica importante de aplicações RAG: **grounding**.

---

## 11. Escopo do MVP

O MVP NÃO terá:

- agentes autônomos;
- múltiplos LLMs;
- sistema complexo de usuários;
- gamificação;
- geração avançada de planos de estudo;
- fine-tuning;
- arquitetura de microserviços;
- infraestrutura distribuída;
- modelo de IA local.

O foco será:

```
Upload
\+
Processamento
\+
Embeddings
\+
Vector Search
\+
RAG
\+
Chat
\+
Citações
```

A prioridade é construir corretamente o pipeline antes de adicionar funcionalidades.

---

## 12. Roadmap

### Fase 1 — Base

- configurar projeto;
- criar backend FastAPI;
- configurar PostgreSQL;
- configurar pgvector;
- criar frontend;
- criar estrutura inicial da aplicação.

### Fase 2 — Document Processing

- upload;
- extração de texto;
- limpeza;
- chunking;
- armazenamento dos documentos.

### Fase 3 — Embeddings

- integração com modelo de embeddings;
- geração dos vetores;
- armazenamento no pgvector.

### Fase 4 — RAG

- busca semântica;
- recuperação Top-K;
- construção de contexto;
- integração com LLM;
- respostas fundamentadas.

### Fase 5 — Interface

- biblioteca de documentos;
- organização por tecnologia;
- chat;
- exibição das fontes.

### Fase 6 — Qualidade

- tratamento de erros;
- validação das respostas;
- avaliação do retrieval;
- testes;
- logging;
- documentação.

### Fase 7 — Evolução

- reranking;
- Explain Mode;
- Study Mode;
- Code Assistant;
- histórico;
- analytics.

---

## 13. Objetivos de aprendizado

O projeto será utilizado principalmente como projeto de estudo e portfólio de **AI Engineering**.

Principais conceitos praticados:

- Python aplicado a IA;
- FastAPI;
- APIs REST;
- processamento de documentos;
- chunking;
- embeddings;
- vector databases;
- pgvector;
- semantic search;
- RAG;
- prompt engineering;
- grounded generation;
- citações e fontes;
- avaliação de sistemas RAG;
- integração com LLM APIs;
- Docker;
- arquitetura de aplicações AI;
- integração frontend/backend.

---

## 14. Diferencial técnico

O projeto não pretende ser "um ChatGPT para PDFs".

O foco é construir uma aplicação especializada em **consulta inteligente de documentação técnica**, permitindo trabalhar com fontes controladas e versões específicas.

A principal proposta técnica é:

> **Documentation → Retrieval → Context → LLM → Grounded Answer**

O valor do projeto para o portfólio estará principalmente na implementação dessa arquitetura e na capacidade de demonstrar que o desenvolvedor entende o funcionamento de um sistema RAG além da simples utilização de uma API de LLM.

---

## 15. Visão futura

A longo prazo, o RAG Tech Docs poderá evoluir de uma ferramenta de consulta para uma espécie de **camada inteligente sobre documentação técnica**.

O usuário poderia estudar uma tecnologia inteira dentro da aplicação:

```
Documentação
      ↓
Consulta
      ↓
Explicação
      ↓
Exercício
      ↓
Avaliação
      ↓
Identificação de lacunas
      ↓
Próximo assunto
```

Entretanto, essa visão não faz parte do MVP.

O primeiro objetivo é construir um **RAG sólido e funcional para documentação técnica**.

