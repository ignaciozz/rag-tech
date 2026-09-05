# 📚 O Papel do `main.py` e do FastAPI

> **Pergunta/Dúvida:** *"Para que serve o arquivo `main.py`? O que ele está fazendo no projeto?"*

---

## 1. O que é? (Explicação Simples)

O `main.py` é a **porta de entrada principal (*entrypoint*)** do servidor backend. 

Quando iniciamos o servidor web com o comando:
```bash
uvicorn app.main:app --reload
```
O Uvicorn procura exatamente o arquivo `main.py` e a variável `app` para ligar o motor da aplicação e escutar as conexões de rede.

---

## 2. O que o código atual faz linha por linha?

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. Criação da Aplicação
app = FastAPI(
    title="RAG Tech Docs API",
    description="API para ingestão de documentação técnica e busca semântica fundamentada (RAG).",
    version="0.1.0",
)

# 2. Configuração de CORS (Permissão para o Frontend acessar a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Rotas Iniciais (Endpoints)
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "rag-tech-docs-api", "version": "0.1.0"}

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bem-vindo à API do RAG Tech Docs! Acesse /docs para ver a documentação interativa."}
```

---

## 3. Conceitos Fundamentais

### 🌐 O que é CORS (Cross-Origin Resource Sharing)?
Por padrão de segurança, um navegador bloqueia um site rodando em `http://localhost:3000` (Frontend) de fazer requisições para `http://localhost:8000` (Backend). O middleware de CORS no `main.py` concede essa autorização de acesso.

### 📖 Documentação Automática (Swagger UI)
O FastAPI gera sozinho uma página web interativa de testes. Basta acessar `http://localhost:8000/docs` no navegador para ver e testar todas as rotas da API em tempo real.

---

## 4. Pontos-chave para fixar (Cheat Sheet)

- 📌 **Ponto Único de Entrada:** O `main.py` inicializa a aplicação, configura middlewares de segurança e registra as rotas.
- 📌 **Modularidade:** Conforme o projeto cresce, as rotas detalhadas vão para a pasta `app/api/`, mantendo o `main.py` limpo e fácil de manter.

