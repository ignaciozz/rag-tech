import type { DocumentListItem as DocumentListItemType } from "@/lib/types";
import { getDownloadUrl } from "@/lib/api";

export function DocumentListItem({
  document,
  onDelete,
}: {
  document: DocumentListItemType;
  onDelete: () => void;
}) {
  const isProcessed = document.embeddedChunks === document.totalChunks;

  return (
    <div className="flex items-center justify-between gap-3 border-b border-border py-3 last:border-b-0">
      <a
        href={getDownloadUrl(document.id)}
        className="min-w-0 flex-1 cursor-pointer"
      >
        <p className="truncate text-sm font-medium underline-offset-2 hover:underline">
          {document.title}
        </p>
        <p className="text-xs text-muted">
          {document.technology}
          {document.version ? ` · ${document.version}` : ""} ·{" "}
          {isProcessed
            ? `${document.totalChunks} trecho(s) processados`
            : `${document.embeddedChunks}/${document.totalChunks} processados`}
        </p>
      </a>
      <button
        onClick={onDelete}
        aria-label={`Apagar ${document.title}`}
        className="flex h-7 w-7 shrink-0 cursor-pointer items-center justify-center rounded-full text-muted transition hover:bg-surface hover:text-foreground"
      >
        <svg
          width="13"
          height="13"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <polyline points="3 6 5 6 21 6" />
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
        </svg>
      </button>
    </div>
  );
}
