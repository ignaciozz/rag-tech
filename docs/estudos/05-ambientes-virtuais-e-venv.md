# 📚 Ambientes Virtuais no Python (`.venv`)

> **Pergunta/Dúvida:** *"O que é um ambiente virtual e por que isolamos as dependências do projeto?"*

---

## 1. O que é? (Explicação Simples)

Por padrão, quando você roda `pip install pacote`, o Python instala a biblioteca globalmente no sistema operacional.

Um **Ambiente Virtual (`.venv`)** cria uma pasta isolada (*sandbox*) dedicada exclusivamente ao projeto atual, com sua própria cópia do interpretador Python e de suas bibliotecas.

---

## 2. Por que usamos e qual problema resolve?

### ❌ O problema de instalar tudo globalmente:
Se você tiver dois projetos no mesmo computador:
- Projeto A precisa da biblioteca `pydantic` na versão `1.10`.
- Projeto B (nosso RAG) precisa de `pydantic` na versão `2.6`.
Se instaladas globalmente, uma versão sobrescreve a outra e quebra um dos projetos (*Dependency Hell*).

### ✅ A solução com `.venv`:
Cada projeto vive no seu próprio ambiente isolado, sem interferir no outro nem no Python do sistema operacional.

---

## 3. Comandos Essenciais no Windows (PowerShell)

1. **Criar o ambiente:**
   ```powershell
   python -m venv .venv
   ```
2. **Ativar o ambiente:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   *(Um prefixo `(.venv)` aparecerá na linha de comando).*
3. **Instalar as dependências do projeto:**
   ```powershell
   pip install -r backend/requirements.txt
   ```
4. **Desativar quando terminar:**
   ```powershell
   deactivate
   ```

---

## 4. Pontos-chave para fixar (Cheat Sheet)

- 📌 **Nunca versionar a pasta `.venv`:** A pasta `.venv` deve estar no `.gitignore`. Cada desenvolvedor ou servidor cria seu próprio `.venv` a partir do `requirements.txt`.
- 📌 **Sempre ativar antes de programar:** Antes de rodar comandos como `uvicorn` ou instalar novas libs, certifique-se de que o `(.venv)` está ativo no terminal.

