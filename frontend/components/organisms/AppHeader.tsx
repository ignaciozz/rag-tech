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
            className="flex items-center gap-1.5 text-xs text-muted underline underline-offset-2 hover:text-foreground"
          >
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
              <line x1="19" y1="12" x2="5" y2="12" />
              <polyline points="12 19 5 12 12 5" />
            </svg>
            {navLabel}
          </Link>
        )}
        <ThemeToggle />
      </div>
    </div>
  );
}
