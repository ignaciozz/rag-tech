import { Badge } from "@/components/atoms/Badge";
import type { Source } from "@/lib/types";

// O backend cita as fontes no formato literal "[Fonte N]" dentro do texto
// (ver backend/app/services/rag.py:SYSTEM_PROMPT) — aqui a gente detecta
// essas marcações e transforma em referências visuais discretas.
const CITATION_SPLIT = /(\[Fonte \d+\])/g;
const CITATION_MATCH = /^\[Fonte \d+\]$/;

function renderContent(content: string) {
  return content.split(CITATION_SPLIT).map((part, i) =>
    CITATION_MATCH.test(part) ? (
      <span key={i} className="align-super text-xs text-muted">
        {part.replace("Fonte ", "")}
      </span>
    ) : (
      <span key={i}>{part}</span>
    ),
  );
}

export function AssistantMessage({
  content,
  sources,
}: {
  content: string;
  sources?: Source[];
}) {
  return (
    <div className="flex max-w-[640px] flex-col gap-2.5">
      <p className="text-sm leading-7">{renderContent(content)}</p>
      {sources && sources.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {sources.map((s) => (
            <Badge key={s.n}>
              Fonte {s.n} · {s.doc} · pág. {s.page}
            </Badge>
          ))}
        </div>
      )}
    </div>
  );
}
