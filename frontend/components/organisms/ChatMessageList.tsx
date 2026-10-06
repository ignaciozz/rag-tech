import { UserMessage } from "@/components/molecules/UserMessage";
import { AssistantMessage } from "@/components/molecules/AssistantMessage";
import type { Message } from "@/lib/types";

export function ChatMessageList({
  messages,
  isLoading,
}: {
  messages: Message[];
  isLoading?: boolean;
}) {
  return (
    <div className="flex flex-1 flex-col gap-6 overflow-y-auto px-7 py-6">
      {messages.map((message) =>
        message.role === "user" ? (
          <UserMessage key={message.id} content={message.content} />
        ) : (
          <AssistantMessage
            key={message.id}
            content={message.content}
            sources={message.sources}
          />
        ),
      )}
      {isLoading && (
        <p className="animate-pulse text-sm text-muted" aria-live="polite">
          ...
        </p>
      )}
    </div>
  );
}
