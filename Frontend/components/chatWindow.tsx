import ChatMessage from "./chatMessage";

interface ChatWindowProps {
  messages: { content: string; sender: "user" | "bot" }[];
}

export default function ChatWindow({ messages }: ChatWindowProps) {
  return (
    <div className="flex flex-col overflow-y-auto h-[500px] border p-4 rounded space-y-2">
      {messages.map((msg, i) => (
        <ChatMessage key={i} content={msg.content} sender={msg.sender} />
      ))}
    </div>
  );
}
