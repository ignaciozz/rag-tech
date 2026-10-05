import { ButtonHTMLAttributes } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary";
};

export function Button({
  variant = "primary",
  className = "",
  ...props
}: ButtonProps) {
  const base =
    "rounded-md px-4 py-2 text-sm font-medium transition disabled:opacity-40 disabled:cursor-not-allowed";
  const variants = {
    // Exceção deliberada de contraste: branco sobre --color-accent dá 3.82:1,
    // abaixo do mínimo AA de 4.5:1 para texto. Aceito conscientemente — ver
    // SKILL.md ("Acessibilidade") para o racional e a alternativa (preto,
    // --color-accent-foreground, 5.49:1) caso isso precise ser revertido.
    // hover:brightness em vez de opacity — mudança de opacidade some quase
    // imperceptível num laranja já saturado com texto branco em cima.
    primary: "bg-accent text-white hover:brightness-90",
    secondary:
      "border border-border text-foreground hover:bg-surface",
  };

  return (
    <button className={`${base} ${variants[variant]} ${className}`} {...props} />
  );
}
