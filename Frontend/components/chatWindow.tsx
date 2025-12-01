// components/chatWindow.tsx
"use client";

interface Message {
  content: string;
  sender: "user" | "bot";
  sources?: any[];
}

interface ChatWindowProps {
  messages: Message[];
  className?: string; // ✅ Add this
}

export default function ChatWindow({ messages, className }: ChatWindowProps) {
  return (
    <div className={`flex-1 overflow-y-auto space-y-2 ${className}`}>
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`p-2 rounded-lg max-w-xs break-words ${
            msg.sender === "user"
              ? "bg-yellow-200 text-yellow-900 ml-auto"
              : "bg-white text-gray-800"
          }`}
        >
          {msg.content}
        </div>
      ))}
    </div>
  );
}
