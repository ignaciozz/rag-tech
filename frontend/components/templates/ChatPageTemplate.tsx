import { ReactNode } from "react";

export function ChatPageTemplate({ children }: { children: ReactNode }) {
  return (
    <main className="flex-1 flex items-center justify-center bg-[#e9e9e9] dark:bg-[#050505] p-10">
      {children}
    </main>
  );
}
