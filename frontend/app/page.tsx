import { ChatPageTemplate } from "@/components/templates/ChatPageTemplate";
import { ChatWindow } from "@/components/organisms/ChatWindow";
import type { Message } from "@/lib/types";

// Dados de exemplo — a conexão com POST /api/v1/chat é o próximo passo.
const mockMessages: Message[] = [
  {
    id: "1",
    role: "user",
    content: "O que é injeção de dependências no FastAPI?",
  },
  {
    id: "2",
    role: "assistant",
    content:
      "É um sistema que permite compartilhar lógica — como conexões de banco de dados — entre vários endpoints de forma limpa e reutilizável [Fonte 1]. O FastAPI resolve essas dependências automaticamente antes de executar a função da rota [Fonte 2].",
    sources: [
      { n: 1, doc: "FastAPI", page: 12 },
      { n: 2, doc: "FastAPI", page: 13 },
    ],
  },
  {
    id: "3",
    role: "user",
    content: "Isso funciona parecido com Spring, no Java?",
  },
];

export default function Home() {
  return (
    <ChatPageTemplate>
      <ChatWindow messages={mockMessages} />
    </ChatPageTemplate>
  );
}
