export function UserMessage({ content }: { content: string }) {
  return (
    <div className="self-end max-w-[60%] rounded-lg bg-surface px-3.5 py-2.5 text-sm">
      {content}
    </div>
  );
}
