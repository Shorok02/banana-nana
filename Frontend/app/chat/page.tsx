// // "use client";

// // import { useState } from "react";
// // import ChatWindow from "../../components/chatWindow";
// // import ChatInput from "../../components/chatInput";
// // import FileUploader from "../../components/fileUploader";
// // import AuthButton from "../../components/authButton";
// // import { askQuestion } from "../../lib/api";

// // interface Message {
// //   content: string;
// //   sender: "user" | "bot";
// //   sources?: any[];
// // }

// // export default function ChatPage() {
// //   const [messages, setMessages] = useState<Message[]>([]);

// //   const sendMessage = async (text: string) => {
// //     if (!text.trim()) return;
// //     setMessages(prev => [...prev, { content: text, sender: "user" }]);

// //     try {
// //       const res = await askQuestion({ question: text });
// //       setMessages(prev => [...prev, { content: res.answer, sender: "bot", sources: res.sources }]);
// //     } catch (err) {
// //       setMessages(prev => [...prev, { content: "Error contacting service", sender: "bot" }]);
// //     }
// //   };

// //   return (
// //     <div className="flex flex-col h-screen bg-gradient-to-b from-yellow-50 to-yellow-100">
// //       {/* Header */}
// //       <header className="flex items-center justify-between p-4 bg-yellow-400 shadow-md">
// //         <h1 className="text-2xl font-extrabold text-white">🍌 Banana-Nana AI</h1>
// //         <AuthButton />
// //       </header>

// //       {/* Main content */}
// //       <main className="flex flex-col flex-1 max-w-3xl mx-auto p-4 space-y-4 overflow-hidden">
// //         {/* File uploader */}
// //         <FileUploader />

// //         {/* Chat window */}
// //         <div className="flex-1 overflow-y-auto rounded-lg bg-white shadow-inner p-4">
// //           <ChatWindow messages={messages} />
// //         </div>

// //         {/* Input box */}
// //         <div className="mt-2">
// //           <ChatInput onSend={sendMessage} />
// //         </div>
// //       </main>
// //     </div>
// //   );
// // }

// "use client";

// import { useState } from "react";
// import ChatWindow from "../../components/chatWindow";
// import ChatInput from "../../components/chatInput";
// import FileUploader from "../../components/fileUploader";
// import AuthButton from "../../components/authButton";
// import { askQuestion } from "../../lib/api";

// interface Message {
//   content: string;
//   sender: "user" | "bot";
//   sources?: any[];
// }



// export default function ChatPage() {
//   const [messages, setMessages] = useState<Message[]>([]);

//   const sendMessage = async (text: string) => {
//     if (!text.trim()) return;

//     setMessages(prev => [...prev, { content: text, sender: "user" }]);

//     try {
//       const res = await askQuestion({ question: text });
//       setMessages(prev => [...prev, { content: res.answer, sender: "bot", sources: res.sources }]);
//     } catch {
//       setMessages(prev => [...prev, { content: "Error: failed to get response", sender: "bot" }]);
//     }
//   };

//   return (
//     <div className="flex h-screen bg-yellow-50">
//       {/* Chat area */}
//       <div className="flex-1 flex flex-col p-6">
//         <div className="flex justify-between items-center mb-4">
//           <h1 className="text-3xl font-bold text-yellow-800">Banana-Nana AI 🍌</h1>
//           <AuthButton />
//         </div>
//         <ChatWindow messages={messages} className="flex-1 overflow-y-auto mb-4" />
//         <ChatInput onSend={sendMessage} />
//       </div>

//       {/* File uploader side panel */}
//       <div className="p-6">
//         <FileUploader />
//       </div>
//     </div>
//   );
// }


"use client";

import { useState } from "react";
import ChatWindow from "../../components/chatWindow";
import ChatInput from "../../components/chatInput";
import FileUploader from "../../components/fileUploader";
import AuthButton from "../../components/authButton";
import { askQuestion } from "../../lib/api";

interface Message {
  content: string;
  sender: "user" | "bot";
  sources?: any[];
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    setMessages(prev => [...prev, { content: text, sender: "user" }]);

    try {
      const res = await askQuestion({ question: text });
      setMessages(prev => [...prev, { content: res.answer, sender: "bot", sources: res.sources }]);
    } catch {
      setMessages(prev => [...prev, { content: "Error: failed to get response", sender: "bot" }]);
    }
  };

  return (
    <div className="flex h-screen bg-yellow-50 p-6 space-x-4">
      {/* File uploader left */}
      <div className="flex-shrink-0">
        <FileUploader />
      </div>

      {/* Chat area right */}
      <div className="flex-1 flex flex-col">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold text-yellow-800">Banana-Nana AI 🍌</h1>
          <AuthButton />
        </div>

        {/* Chat box container */}
        <div className="flex-1 bg-white rounded-xl shadow-md p-4 flex flex-col overflow-y-auto">
          <ChatWindow messages={messages} />
        </div>

        {/* Input box */}
        <div className="mt-2">
          <ChatInput onSend={sendMessage} />
        </div>
      </div>
    </div>
  );
}
