import { CloseButton } from "@/components/atoms/CloseButton";

export function ErrorBanner({
  message,
  onRetry,
  onClose,
}: {
  message: string;
  onRetry: () => void;
  onClose: () => void;
}) {
  return (
    <div
      role="alert"
      className="mb-3 flex items-center justify-between gap-3 rounded-lg border border-border px-3.5 py-2 text-xs text-muted"
    >
      <span>
        {message}{" "}
        <button
          onClick={onRetry}
          className="cursor-pointer underline underline-offset-2 hover:text-foreground"
        >
          Tente novamente
        </button>
      </span>
      <CloseButton aria-label="Fechar aviso" onClick={onClose} />
    </div>
  );
}
