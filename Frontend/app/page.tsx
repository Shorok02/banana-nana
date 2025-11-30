"use client";

import { useState, useRef } from "react";

export default function HomePage() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<File[]>([]);
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<any>(null);

  function openPicker() {
    fileInputRef.current?.click();
  }

  function handleFileSelect(e: React.ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files ? Array.from(e.target.files) : [];
    setFiles(prev => [...prev, ...selected]);  // append not replace
  }

  async function uploadFiles() {
    const formData = new FormData();
    files.forEach(f => formData.append("files", f));

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/files/upload`, {
      method: "POST",
      body: formData,
    }).catch(() => alert("❌ Failed to contact server — check URL + CORS"));

    if (!res) return; // fetch failed entirely

    const data = await res.json();
    alert("Upload results:\n" + JSON.stringify(data, null, 2));
  }

  async function askLLM() {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/qa/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await res.json();
    setResponse(data);
  }

  return (
    <div className="p-10 space-y-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold">Banana-Nana AI 🍌🔍</h1>

      {/* Hidden multiple file input */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        className="hidden"
        onChange={handleFileSelect}
      />

      {/* Upload button */}
      <button
        onClick={openPicker}
        className="bg-black text-white px-4 py-2 rounded"
      >
        + Upload Files
      </button>

      {/* Show selected files */}
      {files.length > 0 && (
        <div className="border p-4 rounded">
          <h3 className="font-semibold mb-2">Selected Files:</h3>
          <ul className="list-disc ml-5 text-sm">
            {files.map((f, i) => <li key={i}>{f.name}</li>)}
          </ul>

          <button
            className="mt-3 bg-blue-600 text-white px-4 py-2 rounded"
            onClick={uploadFiles}
          >
            Upload All
          </button>
        </div>
      )}

      {/* Ask section */}
      <div className="border p-4 rounded space-y-3">
        <input
          className="border p-2 w-full"
          placeholder="Ask your documents..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <button
          onClick={askLLM}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Ask AI
        </button>
      </div>

      {response && (
        <div className="mt-5 border p-4 rounded">
          <h2 className="font-bold text-lg">Answer:</h2>
          <p>{response.answer}</p>

          {response.sources && (
            <>
              <h3 className="mt-3 font-semibold">Sources:</h3>
              <ul className="list-disc ml-5">
                {response.sources.map((src:any, i:number) => (
                  <li key={i}>{src.metadata.filename} — chunk {src.metadata.chunk_index}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}
