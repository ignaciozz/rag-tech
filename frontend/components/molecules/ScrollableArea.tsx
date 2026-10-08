"use client";

import { ReactNode, useEffect, useRef, useState } from "react";

const IDLE_MS = 1000;
const MIN_THUMB_PX = 24;

export function ScrollableArea({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const idleTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [thumb, setThumb] = useState({ top: 0, height: 0 });
  const [visible, setVisible] = useState(false);

  function updateThumb() {
    const el = containerRef.current;
    if (!el) return;
    const { scrollTop, scrollHeight, clientHeight } = el;

    if (scrollHeight <= clientHeight) {
      setThumb({ top: 0, height: 0 }); // conteúdo cabe inteiro: sem barra
      return;
    }

    const thumbHeight = Math.max((clientHeight / scrollHeight) * clientHeight, MIN_THUMB_PX);
    const maxTop = clientHeight - thumbHeight;
    const scrollableDistance = scrollHeight - clientHeight;
    const top = scrollableDistance > 0 ? (scrollTop / scrollableDistance) * maxTop : 0;

    setThumb({ top, height: thumbHeight });
  }

  function handleScroll() {
    updateThumb();
    setVisible(true);
    if (idleTimeout.current) clearTimeout(idleTimeout.current);
    idleTimeout.current = setTimeout(() => setVisible(false), IDLE_MS);
  }

  // Recalcula quando o conteúdo muda de tamanho (ex: lista carregou mais itens).
  useEffect(() => {
    updateThumb();
    return () => {
      if (idleTimeout.current) clearTimeout(idleTimeout.current);
    };
  }, [children]);

  return (
    <div className="relative min-h-0 flex-1">
      <div
        ref={containerRef}
        onScroll={handleScroll}
        className={`scrollbar-hide h-full overflow-y-auto ${className}`}
      >
        {children}
      </div>
      <div
        aria-hidden
        className="pointer-events-none absolute right-0.5 w-1 rounded-full bg-border transition-opacity duration-300 ease-out"
        style={{
          top: thumb.top,
          height: thumb.height,
          opacity: visible && thumb.height > 0 ? 1 : 0,
        }}
      />
    </div>
  );
}
