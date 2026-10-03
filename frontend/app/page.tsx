import { ThemeToggle } from "./theme-toggle";

export default function Home() {
  return (
    <main className="flex-1 flex items-center justify-center bg-[#e9e9e9] dark:bg-[#050505] p-10">
      <div className="w-[820px] h-[680px] flex flex-col overflow-hidden rounded-xl border border-border bg-background shadow-soft">
        {/* Header */}
        <div className="flex h-14 shrink-0 items-center justify-between border-b border-border px-5 backdrop-blur-md">
          <div className="flex items-center gap-2.5">
            <span className="h-2 w-2 rounded-full bg-accent" />
            <span className="text-sm font-semibold tracking-tight">
              RAG Tech Docs
            </span>
          </div>
          <ThemeToggle />
        </div>

        {/* Mensagens */}
        <div className="flex flex-1 flex-col gap-6 overflow-y-auto px-7 py-6">
          <div className="self-end max-w-[60%] rounded-lg bg-surface px-3.5 py-2.5 text-sm">
            O que é injeção de dependências no FastAPI?
          </div>

          <div className="flex max-w-[640px] flex-col gap-2.5">
            <p className="text-sm leading-7">
              É um sistema que permite compartilhar lógica — como conexões de
              banco de dados — entre vários endpoints de forma limpa e
              reutilizável{" "}
              <span className="align-super text-xs text-muted">[1]</span>. O
              FastAPI resolve essas dependências automaticamente antes de
              executar a função da rota{" "}
              <span className="align-super text-xs text-muted">[2]</span>.
            </p>
            <div className="flex flex-wrap gap-2">
              <span className="rounded-full border border-border px-2.5 py-1 text-xs text-muted">
                [1] FastAPI · pág. 12
              </span>
              <span className="rounded-full border border-border px-2.5 py-1 text-xs text-muted">
                [2] FastAPI · pág. 13
              </span>
            </div>
          </div>

          <div className="self-end max-w-[60%] rounded-lg bg-surface px-3.5 py-2.5 text-sm">
            Isso funciona parecido com Spring, no Java?
          </div>
        </div>

        {/* Campo de pergunta */}
        <div className="shrink-0 px-5 pb-5 pt-4">
          <div className="flex items-center gap-2.5 rounded-xl border border-border bg-background py-2.5 pl-4 pr-2.5 shadow-soft">
            <span className="flex-1 text-sm text-muted">
              Pergunte sobre a documentação...
            </span>
            <button
              aria-label="Enviar pergunta"
              className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent text-white"
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
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
