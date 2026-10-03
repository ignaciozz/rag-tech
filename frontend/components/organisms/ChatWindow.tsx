import { ChatHeader } from "@/components/organisms/ChatHeader";
import { ChatMessageList } from "@/components/organisms/ChatMessageList";
import { ChatInput } from "@/components/molecules/ChatInput";
import type { Message } from "@/lib/types";

export function ChatWindow({ messages }: { messages: Message[] }) {
  return (
    <div className="flex h-[680px] w-[820px] flex-col overflow-hidden rounded-xl border border-border bg-background shadow-soft">
      <ChatHeader />
      <ChatMessageList messages={messages} />
      <div className="shrink-0 px-5 pb-5 pt-4">
        <ChatInput />
      </div>
    </div>
  );
}
