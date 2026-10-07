"use client";

import { useEffect, useState } from "react";
import { DocumentListItem } from "@/components/molecules/DocumentListItem";
import { ConfirmDialog } from "@/components/molecules/ConfirmDialog";
import { listDocuments, deleteDocument } from "@/lib/api";
import type { DocumentListItem as DocumentListItemType } from "@/lib/types";

export function DocumentList({ refreshKey }: { refreshKey: number }) {
  const [documents, setDocuments] = useState<DocumentListItemType[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [pendingDelete, setPendingDelete] = useState<DocumentListItemType | null>(null);

  async function load() {
    setIsLoading(true);
    try {
      setDocuments(await listDocuments());
    } catch {
      // Lista é informativa, não crítica — falha aqui não trava o resto da tela.
      setDocuments([]);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshKey]);

  async function handleConfirmDelete() {
    if (!pendingDelete) return;
    await deleteDocument(pendingDelete.id);
    setPendingDelete(null);
    load();
  }

  if (isLoading) {
    return <p className="py-6 text-center text-xs text-muted">Carregando...</p>;
  }

  if (documents.length === 0) {
    return (
      <p className="py-6 text-center text-xs text-muted">
        Nenhum documento cadastrado ainda.
      </p>
    );
  }

  return (
    <div className="min-h-0 flex-1 overflow-y-auto">
      {documents.map((doc) => (
        <DocumentListItem
          key={doc.id}
          document={doc}
          onDelete={() => setPendingDelete(doc)}
        />
      ))}

      {pendingDelete && (
        <ConfirmDialog
          title="Apagar documento?"
          message={`"${pendingDelete.title}" e todos os seus trechos serão removidos permanentemente.`}
          confirmLabel="Apagar"
          cancelLabel="Cancelar"
          onConfirm={handleConfirmDelete}
          onCancel={() => setPendingDelete(null)}
        />
      )}
    </div>
  );
}
