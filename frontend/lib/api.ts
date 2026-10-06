import type { Source } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type ChatResponse = {
  answer: string;
  sources: Source[];
};

export async function askQuestion(question: string): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/api/v1/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error(`A API respondeu com erro (${response.status}).`);
  }

  const data = await response.json();

  // O backend numera as fontes pela ordem de retorno (document_title/page_number),
  // sem um índice explícito — reconstruímos o "n" aqui pra bater com [Fonte N] no texto.
  const sources: Source[] = data.sources.map(
    (s: { document_title: string; technology: string; page_number: number | null }, i: number) => ({
      n: i + 1,
      doc: s.document_title,
      page: s.page_number ?? 0,
    }),
  );

  return { answer: data.answer, sources };
}
