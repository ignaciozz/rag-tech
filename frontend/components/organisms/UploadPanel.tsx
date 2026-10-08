"use client";

import { useState, KeyboardEvent } from "react";
import { Dropzone } from "@/components/molecules/Dropzone";
import { ErrorBanner } from "@/components/molecules/ErrorBanner";
import { ProgressBar } from "@/components/atoms/ProgressBar";
import { IconButton } from "@/components/atoms/IconButton";
import { uploadDocument, embedDocument } from "@/lib/api";

type Stage = "idle" | "configuring" | "uploading" | "embedding" | "done" | "error";

const PROGRESS: Record<Stage, number> = {
  idle: 0,
  configuring: 20,
  uploading: 60,
  embedding: 90,
  done: 100,
  error: 0,
};

function ArrowIcon() {
  return (
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
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>
  );
}

export function UploadPanel({ onUploaded }: { onUploaded?: () => void }) {
  const [stage, setStage] = useState<Stage>("idle");
  const [file, setFile] = useState<File | null>(null);
  const [technology, setTechnology] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [errorStep, setErrorStep] = useState<"upload" | "embed" | null>(null);
  const [documentId, setDocumentId] = useState<string | null>(null);
  const [documentTitle, setDocumentTitle] = useState<string | null>(null);
  const [lastResult, setLastResult] = useState<{
    title: string;
    chunksEmbedded: number;
  } | null>(null);

  function handleFile(selected: File) {
    setFile(selected);
    setStage("configuring");
  }

  async function runEmbed(id: string, title: string) {
    setStage("embedding");
    try {
      const chunksEmbedded = await embedDocument(id);
      setLastResult({ title, chunksEmbedded });
      setStage("done");
      onUploaded?.();
    } catch {
      setErrorStep("embed");
      setError("Documento salvo, mas não consegui gerar os embeddings.");
      setStage("error");
    }
  }

  async function runUpload(selectedFile: File, tech: string) {
    setError(null);
    setStage("uploading");
    try {
      const doc = await uploadDocument(selectedFile, tech, "");
      setDocumentId(doc.id);
      setDocumentTitle(doc.title);
      await runEmbed(doc.id, doc.title);
    } catch {
      setErrorStep("upload");
      setError("Não consegui enviar o documento.");
      setStage("error");
    }
  }

  function handleRetry() {
    if (errorStep === "embed" && documentId && documentTitle) {
      runEmbed(documentId, documentTitle);
    } else if (errorStep === "upload" && file) {
      runUpload(file, technology.trim());
    }
  }

  function handleReset() {
    setStage("idle");
    setFile(null);
    setTechnology("");
    setError(null);
    setErrorStep(null);
    setDocumentId(null);
    setDocumentTitle(null);
  }

  function handleArrowClick() {
    if (file && technology.trim()) {
      runUpload(file, technology.trim());
    }
  }

  function handleInputKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") handleArrowClick();
  }

  const isBusy = stage === "uploading" || stage === "embedding";
  const showForm = stage === "configuring" || isBusy;

  return (
    <div className="flex flex-col items-center gap-5 px-10 py-8">
      <div className="text-center">
        <h1 className="text-lg font-semibold tracking-tight">
          Adicionar documentação
        </h1>
        <p className="mt-1 text-xs text-muted">
          Envie um arquivo para poder fazer perguntas sobre ele no chat.
        </p>
      </div>

      {stage === "idle" && <Dropzone onFile={handleFile} />}

      {stage !== "idle" && (
        <div className="w-full max-w-sm flex flex-col gap-3">
          <p className="truncate text-center text-xs text-muted">{file?.name}</p>
          <ProgressBar percent={PROGRESS[stage]} />

          {showForm && (
            <div className="flex items-center gap-2">
              <input
                autoFocus={stage === "configuring"}
                type="text"
                value={technology}
                onChange={(e) => setTechnology(e.target.value)}
                onKeyDown={handleInputKeyDown}
                disabled={isBusy}
                placeholder="Qual tecnologia?"
                className="flex-1 rounded-md border border-border bg-background px-3 py-2 text-sm placeholder:text-muted focus:outline-none disabled:opacity-60"
              />
              <IconButton
                aria-label="Confirmar tecnologia"
                disabled={isBusy || !file || !technology.trim()}
                onClick={handleArrowClick}
              >
                <ArrowIcon />
              </IconButton>
            </div>
          )}

          {isBusy && (
            <p className="animate-pulse text-center text-xs text-muted" aria-live="polite">
              {stage === "uploading"
                ? "Extraindo e salvando texto..."
                : "Gerando embeddings..."}
            </p>
          )}

          {stage === "done" && lastResult && (
            <div className="flex flex-col items-center gap-2 text-center">
              <p className="text-xs text-muted">
                {lastResult.chunksEmbedded} trecho(s) prontos para consulta.
              </p>
              <button
                onClick={handleReset}
                className="flex cursor-pointer items-center gap-1.5 text-xs text-muted underline underline-offset-2 hover:text-foreground"
              >
                Enviar outro documento
                <svg
                  width="12"
                  height="12"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.25"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <polyline points="8 8 4 12 8 16" />
                  <polyline points="4 12 14 12 14 5" />
                </svg>
              </button>
            </div>
          )}

          {stage === "error" && error && (
            <ErrorBanner
              message={error}
              onRetry={handleRetry}
              onClose={() => setError(null)}
            />
          )}
        </div>
      )}
    </div>
  );
}
