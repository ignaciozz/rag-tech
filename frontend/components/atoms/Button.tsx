import { ButtonHTMLAttributes } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary";
};

export function Button({
  variant = "primary",
  className = "",
  ...props
}: ButtonProps) {
  const base = "rounded-md px-4 py-2 text-sm font-medium transition-colors";
  const variants = {
    // Texto preto sobre o laranja: é o único jeito de manter AA (ver SKILL.md)
    primary: "bg-accent text-accent-foreground hover:opacity-90",
    secondary:
      "border border-border text-foreground hover:bg-surface",
  };

  return (
    <button className={`${base} ${variants[variant]} ${className}`} {...props} />
  );
}
