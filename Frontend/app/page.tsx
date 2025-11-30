// "use client";
// import { useState } from "react";

// type ChatMessage = { type: "user" | "bot"; text: string; sources?: any[] };
// type UploadedFile = { file_id: string; filename: string };

// export default function ChatPage() {
//   const [fileInput, setFileInput] = useState<File | null>(null);
//   const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
//   const [query, setQuery] = useState("");
//   const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);

//   // Upload file
//   async function uploadFile() {
//     if (!fileInput) return;

//     const formData = new FormData();
//     formData.append("files", fileInput); // backend expects "files" array

//     try {
//       const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/files/upload`, {
//         method: "POST",
//         body: formData,
//       });
//       const data = await res.json();
//       if (data.files?.length) {
//         const newFiles = data.files
//           .filter((f: any) => f.status === "queued" || f.status === "processed")
//           .map((f: any) => ({ file_id: f.file_id, filename: f.filename }));
//         setUploadedFiles(prev => [...prev, ...newFiles]);
//       }
//     } catch (err) {
//       console.error("Upload failed", err);
//     } finally {
//       setFileInput(null);
//     }
//   }

//   // Delete file
//   function deleteFile(file_id: string) {
//     setUploadedFiles(prev => prev.filter(f => f.file_id !== file_id));
//     // optionally call backend to delete from Chroma + SQLite
//   }

//   // Ask a question
//   async function askQuestion() {
//     if (!query.trim()) return;

//     setChatHistory(prev => [...prev, { type: "user", text: query }]);
//     setQuery("");

//     try {
//       const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/qa/ask`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ query }),
//       });
//       const data = await res.json();
//       setChatHistory(prev => [
//         ...prev,
//         { type: "bot", text: data.answer, sources: data.sources },
//       ]);
//     } catch (err) {
//       console.error(err);
//       setChatHistory(prev => [
//         ...prev,
//         { type: "bot", text: "Error fetching answer" },
//       ]);
//     }
//   }

//   return (
//     <div className="max-w-3xl mx-auto p-5">
//       <h1 className="text-3xl font-bold mb-4">Banana-Nana Chat Agent</h1>

//       {/* File Upload */}
//       <div className="mb-4">
//         <input
//           type="file"
//           onChange={e => setFileInput(e.target.files?.[0] ?? null)}
//         />
//         <button
//           onClick={uploadFile}
//           disabled={!fileInput}
//           className="ml-2 px-3 py-1 bg-black text-white rounded"
//         >
//           Upload
//         </button>
//       </div>

//       {/* Uploaded Files */}
//       {uploadedFiles.length > 0 && (
//         <div className="mb-4">
//           <h2 className="font-semibold mb-2">Uploaded Files:</h2>
//           <ul>
//             {uploadedFiles.map(f => (
//               <li key={f.file_id} className="flex justify-between items-center">
//                 <span>{f.filename}</span>
//                 <button
//                   onClick={() => deleteFile(f.file_id)}
//                   className="ml-2 px-2 py-1 text-sm bg-red-500 text-white rounded"
//                 >
//                   Delete
//                 </button>
//               </li>
//             ))}
//           </ul>
//         </div>
//       )}

//       {/* Chat Input */}
//       <div className="flex mb-4">
//         <input
//           className="border p-2 flex-1"
//           placeholder="Ask a question..."
//           value={query}
//           onChange={e => setQuery(e.target.value)}
//           onKeyDown={e => e.key === "Enter" && askQuestion()}
//         />
//         <button
//           onClick={askQuestion}
//           className="ml-2 px-4 py-2 bg-blue-500 text-white rounded"
//         >
//           Ask
//         </button>
//       </div>

//       {/* Chat History */}
//       <div className="space-y-3 border p-3 rounded h-96 overflow-y-auto">
//         {chatHistory.map((m, i) => (
//           <div key={i} className={m.type === "user" ? "text-right" : "text-left"}>
//             <p className={`inline-block p-2 rounded ${
//               m.type === "user" ? "bg-blue-500 text-white" : "bg-gray-200"
//             }`}>
//               {m.text}
//             </p>
//             {m.sources && m.sources.length > 0 && (
//               <ul className="text-xs ml-1 mt-1">
//                 {m.sources.map((s, j) => (
//                   <li key={j}>
//                     {s.metadata.filename} — chunk {s.metadata.chunk_index}
//                   </li>
//                 ))}
//               </ul>
//             )}
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }

"use client";

import { useState } from "react";
import ChatWindow from "../components/chatWindow";
import ChatInput from "../components/chatInput";
import FileUploader from "../components/fileUploader";
import { askQuestion } from "../lib/api";

interface Message {
  content: string;
  sender: "user" | "bot";
  sources?: any[];
}

export default function HomePage() {
  const [messages, setMessages] = useState<Message[]>([]);

  // Send a user question to backend
  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    // Add user message to chat
    setMessages(prev => [...prev, { content: text, sender: "user" }]);

    try {
      // Call API with correct payload { question: "...", k: optional }
      const res = await askQuestion({ question: text });

      // Add bot response to chat
      setMessages(prev => [...prev, { content: res.answer, sender: "bot", sources: res.sources }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [
        ...prev,
        { content: "Error: failed to get response", sender: "bot" }
      ]);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-3xl font-bold">Banana-Nana AI</h1>

      {/* File uploader component */}
      <FileUploader />

      {/* Chat messages */}
      <ChatWindow messages={messages} />

      {/* Input box */}
      <ChatInput onSend={sendMessage} />
    </div>
  );
}

