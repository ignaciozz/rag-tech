import type { DocumentInfo, DocumentListItem, Source } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const TIMEOUT_MS = 30_000;

// Usado direto num <a href>, não via fetch — o backend já manda
// Content-Disposition: attachment, então o navegador baixa sozinho.
export function getDownloadUrl(documentId: string): string {
  return `${API_URL}/api/v1/documents/${documentId}/download`;
}

// fetch() não tem timeout embutido — sem isso, se o backend cair ou travar
// no meio de uma requisição, a Promise nunca resolve nem rejeita, e a UI
// fica presa num estado de carregamento pra sempre, sem erro nenhum.
async function fetchWithTimeout(input: string, init?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    return await fetch(input, { ...init, signal: controller.signal });
  } catch (err) {
    if (err instanceof Error && err.name === "AbortError") {
      throw new Error("O servidor demorou demais para responder.");
    }
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

export type ChatResponse = {
  answer: string;
  sources: Source[];
};

export async function askQuestion(question: string): Promise<ChatResponse> {
  const response = await fetchWithTimeout(`${API_URL}/api/v1/chat`, {
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

export async function uploadDocument(
  file: File,
  technology: string,
  version: string,
): Promise<DocumentInfo> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("technology", technology);
  if (version) formData.append("version", version);

  const response = await fetchWithTimeout(`${API_URL}/api/v1/documents/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Falha no upload (${response.status}).`);
  }

  const data = await response.json();
  return {
    id: data.id,
    title: data.title,
    technology: data.technology,
    version: data.version,
    fileType: data.file_type,
    chunksCount: data.chunks_count,
  };
}

export async function listDocuments(): Promise<DocumentListItem[]> {
  const response = await fetchWithTimeout(`${API_URL}/api/v1/documents`);

  if (!response.ok) {
    throw new Error(`Falha ao listar documentos (${response.status}).`);
  }

  const data = await response.json();
  return data.map(
    (d: {
      id: string;
      title: string;
      technology: string;
      version: string | null;
      file_type: string;
      total_chunks: number;
      embedded_chunks: number;
    }) => ({
      id: d.id,
      title: d.title,
      technology: d.technology,
      version: d.version,
      fileType: d.file_type,
      totalChunks: d.total_chunks,
      embeddedChunks: d.embedded_chunks,
    }),
  );
}

export async function deleteDocument(documentId: string): Promise<void> {
  const response = await fetchWithTimeout(
    `${API_URL}/api/v1/documents/${documentId}`,
    { method: "DELETE" },
  );

  if (!response.ok) {
    throw new Error(`Falha ao apagar documento (${response.status}).`);
  }
}

export async function embedDocument(documentId: string): Promise<number> {
  const response = await fetchWithTimeout(
    `${API_URL}/api/v1/documents/${documentId}/embed`,
    { method: "POST" },
  );

  if (!response.ok) {
    throw new Error(`Falha ao gerar embeddings (${response.status}).`);
  }

  const data = await response.json();
  return data.chunks_embedded;
}
