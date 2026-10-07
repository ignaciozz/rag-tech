import openai


class AIProviderError(Exception):
    """
    Erro ao se comunicar com o provedor de IA (embeddings ou chat).
    Lançada pelos services (embedder.py, rag.py), traduzida para HTTP
    pelos endpoints — mantém os services sem dependência do FastAPI.
    """


def translate_openai_error(error: openai.APIError) -> AIProviderError:
    """
    Traduz uma exceção do SDK da OpenAI (que também cobre provedores
    compatíveis, como o Gemini) para uma mensagem clara e acionável.
    """
    if isinstance(error, openai.AuthenticationError):
        return AIProviderError(
            "Chave de API inválida ou ausente. Verifique AI_API_KEY no .env."
        )
    if isinstance(error, openai.RateLimitError):
        return AIProviderError(
            "Limite de requisições do provedor de IA excedido. Tente novamente em instantes."
        )
    if isinstance(error, openai.NotFoundError):
        return AIProviderError(
            "Modelo de IA não encontrado — pode ter sido descontinuado. "
            "Verifique EMBEDDING_MODEL/CHAT_MODEL no .env."
        )
    if isinstance(error, openai.APIConnectionError):
        return AIProviderError(
            "Não foi possível conectar ao provedor de IA. Verifique sua conexão e AI_BASE_URL."
        )
    if isinstance(error, openai.InternalServerError):
        return AIProviderError(
            "O provedor de IA está sobrecarregado ou indisponível no momento "
            f"(comum em tiers gratuitos). Tente novamente em instantes. Detalhe: {error}"
        )
    if isinstance(error, openai.BadRequestError):
        # Alguns provedores compatíveis (ex: Gemini) devolvem 400 em vez de 401
        # para chave de API inválida, diferente do padrão da própria OpenAI.
        return AIProviderError(
            "Requisição rejeitada pelo provedor de IA — verifique se AI_API_KEY é válida "
            f"e se os modelos configurados existem. Detalhe original: {error}"
        )
    return AIProviderError(f"Erro inesperado do provedor de IA: {error}")
