interface ChatMessageProps {
  content: string;
  sender: "user" | "bot";
}

export default function ChatMessage({ content, sender }: ChatMessageProps) {
  return (
    <div className={`flex ${sender === "user" ? "justify-end" : "justify-start"} mb-2`}>
      <div className={`p-3 rounded-lg max-w-xs ${
        sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-900"
      }`}>
        {content}
      </div>
    </div>
  );
}
