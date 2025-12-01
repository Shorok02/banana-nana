
"use client";

import { useState } from "react";

interface Props {
  onSend: (text: string) => void;
}

export default function ChatInput({ onSend }: Props) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <div className="flex space-x-2">
      <input
        type="text"
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Ask Banana-Nana AI something..."
        className="flex-1 rounded-xl px-4 py-2 border border-yellow-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"
      />
      <button
        onClick={handleSend}
        className="bg-yellow-400 hover:bg-yellow-500 text-white px-4 py-2 rounded-xl font-semibold"
      >
        Send
      </button>
    </div>
  );
}
