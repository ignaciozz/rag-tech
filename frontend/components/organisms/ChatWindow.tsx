"use client";

import { useState } from "react";
import { ChatHeader } from "@/components/organisms/ChatHeader";
import { ChatMessageList } from "@/components/organisms/ChatMessageList";
import { ChatInput } from "@/components/molecules/ChatInput";
import { ErrorBanner } from "@/components/molecules/ErrorBanner";
import { askQuestion } from "@/lib/api";
import type { Message } from "@/lib/types";

export function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastQuestion, setLastQuestion] = useState<string | null>(null);

  async function fetchAnswer(question: string) {
    setError(null);
    setIsLoading(true);

    try {
      const { answer, sources } = await askQuestion(question);
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: "assistant", content: answer, sources },
      ]);
    } catch {
      // Erro de rede/servidor — diferente de uma recusa por falta de evidência,
      // que o backend devolve como resposta normal em `answer`, não como exceção.
      setError("Não consegui falar com o servidor.");
    } finally {
      setIsLoading(false);
    }
  }

  function handleSend(question: string) {
    setLastQuestion(question);
    setMessages((prev) => [
      ...prev,
      { id: crypto.randomUUID(), role: "user", content: question },
    ]);
    fetchAnswer(question);
  }

  function handleRetry() {
    if (lastQuestion) fetchAnswer(lastQuestion);
  }

  return (
    <div className="flex h-[680px] w-[820px] flex-col overflow-hidden rounded-xl border border-border bg-background shadow-soft">
      <ChatHeader />

      {messages.length === 0 && !isLoading ? (
        <div className="flex flex-1 flex-col items-center justify-center gap-1 px-7 text-center">
          <p className="text-sm font-medium">
            Pergunte algo sobre a documentação que você já cadastrou.
          </p>
          <p className="text-xs text-muted">
            As respostas citam a página exata de onde vieram.
          </p>
        </div>
      ) : (
        <ChatMessageList messages={messages} isLoading={isLoading} />
      )}

      <div className="shrink-0 px-5 pb-5 pt-4">
        {error && (
          <ErrorBanner
            message={error}
            onRetry={handleRetry}
            onClose={() => setError(null)}
          />
        )}
        <ChatInput onSend={handleSend} disabled={isLoading} />
      </div>
    </div>
  );
}
