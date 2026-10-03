import { ButtonHTMLAttributes } from "react";

type IconButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  "aria-label": string; // obrigatório: botão só-ícone precisa de nome acessível
};

export function IconButton({ className = "", ...props }: IconButtonProps) {
  return (
    <button
      // Ícone branco sobre laranja: passa no mínimo de contraste de elemento
      // gráfico (3:1), diferente do texto (4.5:1) — ver SKILL.md.
      className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent text-white transition-opacity hover:opacity-90 disabled:opacity-40 ${className}`}
      {...props}
    />
  );
}
