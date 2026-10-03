import { ThemeToggle } from "@/components/atoms/ThemeToggle";

export function ChatHeader() {
  return (
    <div className="flex h-14 shrink-0 items-center justify-between border-b border-border px-5 backdrop-blur-md">
      <div className="flex items-center gap-2.5">
        <span className="h-2 w-2 rounded-full bg-accent" />
        <span className="text-sm font-semibold tracking-tight">
          RAG Tech Docs
        </span>
      </div>
      <ThemeToggle />
    </div>
  );
}
