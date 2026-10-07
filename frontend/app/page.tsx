import { ChatPageTemplate } from "@/components/templates/ChatPageTemplate";
import { DocumentManager } from "@/components/organisms/DocumentManager";

export default function Home() {
  return (
    <ChatPageTemplate>
      <DocumentManager />
    </ChatPageTemplate>
  );
}
