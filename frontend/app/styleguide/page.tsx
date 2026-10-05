import { Button } from "@/components/atoms/Button";
import { IconButton } from "@/components/atoms/IconButton";
import { Badge } from "@/components/atoms/Badge";
import { ThemeToggle } from "@/components/atoms/ThemeToggle";
import { UserMessage } from "@/components/molecules/UserMessage";
import { AssistantMessage } from "@/components/molecules/AssistantMessage";
import { ChatInput } from "@/components/molecules/ChatInput";
import { ChatHeader } from "@/components/organisms/ChatHeader";

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="flex flex-col gap-4 border-b border-border py-10">
      <h2 className="text-xs font-semibold uppercase tracking-wide text-muted">
        {title}
      </h2>
      {children}
    </section>
  );
}

function Swatch({ name, className }: { name: string; className: string }) {
  return (
    <div className="flex flex-col gap-2">
      <div
        className={`h-16 w-full rounded-md border border-border ${className}`}
      />
      <span className="text-xs font-medium">{name}</span>
    </div>
  );
}

function RadiusSample({ name, className }: { name: string; className: string }) {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className={`h-14 w-14 border border-border bg-surface ${className}`} />
      <span className="text-xs text-muted">{name}</span>
    </div>
  );
}

export default function Styleguide() {
  return (
    <main className="mx-auto max-w-3xl px-6">
      <div className="flex items-center justify-between py-10">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Design System
          </h1>
          <p className="mt-1 text-sm text-muted">
            RAG Tech Docs — tokens e componentes ao vivo (Atomic Design).
          </p>
        </div>
        <ThemeToggle />
      </div>

      <Section title="Cores">
        <div className="grid grid-cols-3 gap-4 sm:grid-cols-6">
          <Swatch name="background" className="bg-background" />
          <Swatch name="foreground" className="bg-foreground" />
          <Swatch name="muted" className="bg-muted" />
          <Swatch name="border" className="bg-border" />
          <Swatch name="surface" className="bg-surface" />
          <Swatch name="accent" className="bg-accent" />
        </div>
      </Section>

      <Section title="Tipografia — Poppins">
        <div className="flex flex-col gap-3">
          <p className="text-3xl font-bold tracking-tight">RAG Tech Docs</p>
          <p className="text-xl font-semibold">Título de seção</p>
          <p className="max-w-prose text-sm leading-7">
            O FastAPI usa injeção de dependências para compartilhar lógica
            entre endpoints de forma limpa e reutilizável.
          </p>
          <p className="text-sm text-muted">Texto secundário / muted.</p>
        </div>
      </Section>

      <Section title="Raio de borda & elevação">
        <div className="flex flex-wrap items-end gap-8">
          <RadiusSample name="sm · 6px" className="rounded-sm" />
          <RadiusSample name="md · 10px" className="rounded-md" />
          <RadiusSample name="lg · 16px" className="rounded-lg" />
          <RadiusSample name="xl · 20px" className="rounded-xl" />
          <div className="flex flex-col items-center gap-2">
            <div className="h-14 w-32 rounded-lg border border-border bg-background shadow-soft" />
            <span className="text-xs text-muted">shadow-soft</span>
          </div>
        </div>
      </Section>

      <Section title="Átomos — Button">
        <div className="flex gap-3">
          <Button variant="primary">Perguntar</Button>
          <Button variant="secondary">Cancelar</Button>
          <Button variant="primary" disabled>
            Desabilitado
          </Button>
        </div>
      </Section>

      <Section title="Átomos — IconButton">
        <div className="flex items-center gap-3">
          <IconButton aria-label="Enviar pergunta">
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
          <span className="text-xs text-muted">
            Ícone branco sobre laranja — só permitido sem texto ao lado (ver
            SKILL.md).
          </span>
        </div>
      </Section>

      <Section title="Átomos — Badge">
        <div className="flex flex-wrap gap-2">
          <Badge>Fonte 1 · FastAPI · pág. 12</Badge>
          <Badge>Fonte 2 · PostgreSQL · pág. 4</Badge>
        </div>
      </Section>

      <Section title="Átomos — ThemeToggle">
        <ThemeToggle />
      </Section>

      <Section title="Moléculas — Mensagens">
        <div className="flex flex-col gap-4 rounded-lg border border-border p-5">
          <UserMessage content="O que é injeção de dependências no FastAPI?" />
          <AssistantMessage
            content="É um sistema que permite compartilhar lógica entre endpoints [Fonte 1]."
            sources={[{ n: 1, doc: "FastAPI", page: 12 }]}
          />
        </div>
      </Section>

      <Section title="Moléculas — ChatInput">
        <ChatInput />
      </Section>

      <Section title="Organismos — ChatHeader">
        <div className="overflow-hidden rounded-lg border border-border">
          <ChatHeader />
        </div>
      </Section>

      <p className="py-10 text-xs text-muted">
        Organismo ChatWindow e template ChatPageTemplate: ver a tela de chat
        completa em <code className="text-foreground">/</code>.
      </p>
    </main>
  );
}
