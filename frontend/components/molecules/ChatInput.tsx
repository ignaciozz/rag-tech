"use client";

import { useState, FormEvent } from "react";
import { IconButton } from "@/components/atoms/IconButton";

export function ChatInput({
  onSend,
  disabled,
}: {
  onSend: (question: string) => void;
  disabled?: boolean;
}) {
  const [value, setValue] = useState("");

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const question = value.trim();
    if (!question || disabled) return;
    onSend(question);
    setValue("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center gap-2.5 rounded-xl border border-border bg-background py-2.5 pl-4 pr-2.5 shadow-soft"
    >
      <label htmlFor="question" className="sr-only">
        Pergunte sobre a documentação
      </label>
      <input
        id="question"
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        disabled={disabled}
        placeholder="Pergunte sobre a documentação..."
        className="flex-1 bg-transparent text-sm text-foreground placeholder:text-muted focus:outline-none disabled:opacity-60"
      />
      <IconButton
        type="submit"
        aria-label="Enviar pergunta"
        disabled={disabled || !value.trim()}
      >
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <line x1="12" y1="19" x2="12" y2="5" />
          <polyline points="5 12 12 5 19 12" />
        </svg>
      </IconButton>
    </form>
  );
}
