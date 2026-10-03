"use client";

import { useEffect, useState } from "react";
import { useTheme } from "next-themes";

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  // Evita mismatch de hidratação: no primeiro render do servidor não sabemos
  // ainda qual tema o navegador prefere.
  useEffect(() => setMounted(true), []);
  if (!mounted) return null;

  const isDark = resolvedTheme === "dark";

  return (
    <button
      onClick={() => setTheme(isDark ? "light" : "dark")}
      className="rounded-md border border-border px-3 py-1.5 text-xs text-foreground hover:bg-surface"
    >
      {isDark ? "Modo claro" : "Modo escuro"}
    </button>
  );
}
