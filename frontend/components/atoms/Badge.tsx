import { ReactNode } from "react";

export function Badge({ children }: { children: ReactNode }) {
  return (
    <span className="rounded-full border border-border px-2.5 py-1 text-xs text-muted">
      {children}
    </span>
  );
}
