import { ButtonHTMLAttributes } from "react";

type CloseButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  "aria-label": string;
};

export function CloseButton({ className = "", ...props }: CloseButtonProps) {
  return (
    <button
      // Neutro, nunca laranja — fechar não é a ação primária da tela.
      className={`flex h-6 w-6 shrink-0 cursor-pointer items-center justify-center rounded-full text-muted transition hover:bg-surface hover:text-foreground ${className}`}
      {...props}
    >
      <svg
        width="12"
        height="12"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      </svg>
    </button>
  );
}
