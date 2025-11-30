"use client";

import { useState } from "react";
import { apiGet, apiPost } from "../lib/api";

interface FileMeta {
  name: string;
  size: number;
}

export default function FileUploader() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [processedDocs, setProcessedDocs] = useState<any[]>([]);

  // Add files from file input
  const addFiles = (files: FileList | null) => {
    if (!files) return;
    setSelectedFiles(prev => [...prev, ...Array.from(files)]);
  };

  // Remove single file from selection
  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  // Upload files to backend
  const uploadFiles = async () => {
    if (selectedFiles.length === 0) return alert("Select files first");

    const formData = new FormData();
    selectedFiles.forEach(f => formData.append("files", f));

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/upload`, {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      alert("Files uploaded successfully");
      setSelectedFiles([]); // reset after upload
    } catch (err) {
      console.error(err);
      alert("Failed to upload files");
    }
  };

  // Fetch processed documents from backend
  const fetchDocs = async () => {
    const docs = await apiGet("/api/docs");
    setProcessedDocs(docs);
  };

  return (
    <div className="border p-4 rounded space-y-3">
      <label className="flex items-center cursor-pointer text-blue-600">
        <span className="text-2xl mr-2">+</span> Add files
        <input
          type="file"
          multiple
          className="hidden"
          onChange={e => addFiles(e.target.files)}
        />
      </label>

      {selectedFiles.length > 0 && (
        <ul className="list-disc ml-6">
          {selectedFiles.map((file, i) => (
            <li key={i} className="flex justify-between items-center">
              {file.name} ({(file.size / 1024).toFixed(1)} KB)
              <button
                className="text-red-500 ml-2"
                onClick={() => removeFile(i)}
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}

      <div className="flex space-x-2">
        <button
          className="bg-green-500 text-white px-4 py-2 rounded"
          onClick={uploadFiles}
        >
          Upload
        </button>
        <button
          className="bg-gray-200 px-4 py-2 rounded"
          onClick={fetchDocs}
        >
          Show Processed Docs
        </button>
      </div>

      {processedDocs.length > 0 && (
        <div className="mt-3">
          <h3 className="font-semibold">Processed Documents:</h3>
          <ul className="list-disc ml-6 text-sm text-gray-700">
            {processedDocs.map(doc => (
              <li key={doc.id}>
                {doc.filename} — Chunks: {doc.chunks_count}, Embeddings: {doc.embeddings_count}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
