// // components/chatWindow.tsx
// "use client";

// interface Message {
//   content: string;
//   sender: "user" | "bot";
//   sources?: any[];
// }

// interface ChatWindowProps {
//   messages: Message[];
//   className?: string; // ✅ Add this
// }

// export default function ChatWindow({ messages, className }: ChatWindowProps) {
//   return (
//     <div className={`flex-1 overflow-y-auto space-y-2 ${className}`}>
//       {messages.map((msg, idx) => (
//         <div
//           key={idx}
//           className={`p-2 rounded-lg max-w-xs break-words ${
//             msg.sender === "user"
//               ? "bg-yellow-200 text-yellow-900 ml-auto"
//               : "bg-white text-gray-800"
//           }`}
//         >
//           {msg.content}
//         </div>
//       ))}
//     </div>
//   );
// }




// "use client";

// interface Message {
//   content: string;
//   sender: "user" | "bot";
//   sources?: { title?: string; url?: string }[]; // optional sources with title/url
// }

// interface ChatWindowProps {
//   messages: Message[];
//   className?: string;
// }

// export default function ChatWindow({ messages, className }: ChatWindowProps) {
//   return (
//     <div className={`flex-1 overflow-y-auto space-y-2 ${className}`}>
//       {messages.map((msg, idx) => (
//         <div
//           key={idx}
//           className={`p-2 rounded-lg max-w-xs break-words ${
//             msg.sender === "user"
//               ? "bg-yellow-200 text-yellow-900 ml-auto"
//               : "bg-white text-gray-800"
//           }`}
//         >
//           <div>{msg.content}</div>

//           {/* Render sources only for bot messages */}
//           {msg.sender === "bot" && msg.sources && msg.sources.length > 0 && (
//             <div className="mt-2 text-sm text-gray-500 border-t border-gray-200 pt-1">
//               <div className="font-semibold mb-1">Sources:</div>
//               <ul className="list-disc pl-5 space-y-1">
//                 {msg.sources.map((src, i) => (
//                   <li key={i}>
//                     {src.url ? (
//                       <a
//                         href={src.url}
//                         target="_blank"
//                         rel="noopener noreferrer"
//                         className="underline text-blue-600"
//                       >
//                         {src.title|| src.url}
//                       </a>
//                     ) : (
//                       src.title || "Unknown source"
//                     )}
//                   </li>
//                 ))}
//               </ul>
//             </div>
//           )}
//         </div>
//       ))}
//     </div>
//   );
// }

"use client";

interface Source {
  metadata?: {
    filename?: string;
    chunk_index?: number;
  };
}

interface Message {
  content: string;
  sender: "user" | "bot";
  sources?: Source[];
}

interface ChatWindowProps {
  messages: Message[];
  className?: string;
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
          <div>{msg.content}</div>

          {/* Show sources only for bot messages */}
          {msg.sender === "bot" && msg.sources && msg.sources.length > 0 && (
            <div className="mt-2 text-sm text-gray-500 border-t border-gray-200 pt-1">
              <div className="font-semibold mb-1">Sources:</div>
              <ul className="list-disc pl-5 space-y-1">
                {msg.sources.map((src, i) => {
                  const filename = src.metadata?.filename || "Unknown file";
                  const chunkIndex = src.metadata?.chunk_index ?? "?";
                  return (
                    <li key={i}>
                      {filename} (chunk {chunkIndex})
                    </li>
                  );
                })}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
