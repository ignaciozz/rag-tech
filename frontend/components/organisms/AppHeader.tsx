import Link from "next/link";
import { MouseEvent } from "react";
import { ThemeToggle } from "@/components/atoms/ThemeToggle";

export function AppHeader({
  navLabel,
  navHref,
  onNavClick,
}: {
  navLabel?: string;
  navHref?: string;
  onNavClick?: (e: MouseEvent<HTMLAnchorElement>) => void;
}) {
  return (
    <div className="flex h-14 shrink-0 items-center justify-between border-b border-border px-5 backdrop-blur-md">
      <div className="flex items-center gap-2.5">
        <span className="h-2 w-2 rounded-full bg-accent" />
        <span className="text-sm font-semibold tracking-tight">
          RAG Tech Docs
        </span>
      </div>
      <div className="flex items-center gap-4">
        {navLabel && navHref && (
          <Link
            href={navHref}
            onClick={onNavClick}
            className="text-xs text-muted underline underline-offset-2 hover:text-foreground"
          >
            {navLabel}
          </Link>
        )}
        <ThemeToggle />
      </div>
    </div>
  );
}
