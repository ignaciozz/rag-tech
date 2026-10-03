import { ThemeToggle } from "./theme-toggle";

export default function Home() {
  return (
    <main className="flex-1 flex flex-col items-center justify-center gap-6 p-8">
      <ThemeToggle />

      <h1 className="text-3xl font-semibold tracking-tight">
        RAG Tech Docs
      </h1>
      <p className="max-w-prose text-center text-muted">
        Design system em verificação — cores, tipografia (Poppins) e modo
        claro/escuro.
      </p>

      <button className="rounded bg-accent px-4 py-2 font-medium text-accent-foreground">
        Perguntar
      </button>

      <div className="rounded border border-border px-4 py-3 text-sm text-muted">
        [Fonte 1] — FastAPI, página 3
      </div>
    </main>
  );
}
