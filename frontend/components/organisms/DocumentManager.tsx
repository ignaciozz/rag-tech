"use client";

import { useState } from "react";
import { AppHeader } from "@/components/organisms/AppHeader";
import { UploadPanel } from "@/components/organisms/UploadPanel";
import { DocumentList } from "@/components/organisms/DocumentList";

export function DocumentManager() {
  // Incrementar isso re-dispara a busca da lista no DocumentList (useEffect por refreshKey).
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="flex h-[680px] w-[820px] flex-col overflow-hidden rounded-xl border border-border bg-background shadow-soft">
      <AppHeader navLabel="Chat" navHref="/chat" />

      <div className="shrink-0">
        <UploadPanel onUploaded={() => setRefreshKey((k) => k + 1)} />
      </div>

      <div className="flex min-h-0 flex-1 flex-col border-t border-border px-8 py-4">
        <h2 className="mb-2 shrink-0 text-xs font-semibold uppercase tracking-wide text-muted">
          Documentos cadastrados
        </h2>
        <DocumentList refreshKey={refreshKey} />
      </div>
    </div>
  );
}
