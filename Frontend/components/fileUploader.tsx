// // // "use client";

// // // import { useState } from "react";
// // // import { getSession } from "next-auth/react";

// // // interface FileUploaderProps {
// // //   fetchDocs?: () => void;
// // // }

// // // export default function FileUploader() {
// // //   const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
// // //   const [processedDocs, setProcessedDocs] = useState<any[]>([]);
// // //   const [loading, setLoading] = useState(false);

// // //   // Add files reliably
// // //   const addFiles = (files: FileList | null) => {
// // //     if (!files) return;
// // //     setSelectedFiles(prev => {
// // //       const newFiles = Array.from(files);
// // //       const merged = [...prev];
// // //       newFiles.forEach(f => {
// // //         if (!merged.some(x => x.name === f.name && x.size === f.size)) merged.push(f);
// // //       });
// // //       return merged;
// // //     });
// // //   };

// // //   // Upload files with auth token
// // //   const uploadFiles = async () => {
// // //     if (selectedFiles.length === 0) return alert("Select files first");
// // //     setLoading(true);

// // //     const session = await getSession();
// // //     const token = (session as any)?.idToken;
// // //     if (!token) {
// // //       alert("Login required");
// // //       setLoading(false);
// // //       return;
// // //     }

// // //     const formData = new FormData();
// // //     selectedFiles.forEach(f => formData.append("files", f));

// // //     try {
// // //       const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/upload`, {
// // //         method: "POST",
// // //         body: formData,
// // //         headers: {
// // //           Authorization: `Bearer ${token}`,
// // //         },
// // //       });

// // //       const data = await res.json();
// // //       alert("Upload complete!");
// // //       setSelectedFiles([]);
// // //     } catch (err) {
// // //       console.error(err);
// // //       alert("Upload failed");
// // //     }

// // //     setLoading(false);
// // //     if (fetchDocs) fetchDocs();
// // //   };

// // //   const fetchDocs = async () => {
// // //     const session = await getSession();
// // //     const token = (session as any)?.idToken;
// // //     if (!token) return alert("Login first");

// // //     const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/docs`, {
// // //       headers: { Authorization: `Bearer ${token}` },
// // //     });

// // //     setProcessedDocs(await res.json());
// // //   };

// // //   return (
// // //     <div className="bg-yellow-50 p-5 rounded-xl shadow-md border border-yellow-200 space-y-4">
// // //       <h2 className="text-xl font-bold text-yellow-700 flex items-center">
// // //         🍌 Upload Files
// // //       </h2>

// // //       {/* File input */}
// // //       <label className="flex items-center justify-center cursor-pointer text-yellow-600 font-semibold p-3 border-2 border-dashed border-yellow-400 rounded-xl hover:bg-yellow-100 transition">
// // //         <span className="text-2xl mr-2">+</span> Select Files
// // //         <input type="file" multiple className="hidden" onChange={e => addFiles(e.target.files)} />
// // //       </label>

// // //       {/* Selected files */}
// // //       {selectedFiles.length > 0 && (
// // //         <ul className="list-disc ml-6 text-gray-700 space-y-1">
// // //           {selectedFiles.map((file, i) => (
// // //             <li key={i} className="flex justify-between items-center">
// // //               {file.name} ({(file.size / 1024).toFixed(1)} KB)
// // //               <button
// // //                 className="text-red-500 ml-3 hover:underline"
// // //                 onClick={() => setSelectedFiles(prev => prev.filter((_, idx) => idx !== i))}
// // //               >
// // //                 Remove
// // //               </button>
// // //             </li>
// // //           ))}
// // //         </ul>
// // //       )}

// // //       {/* Action buttons */}
// // //       <div className="flex space-x-2">
// // //         <button
// // //           className="bg-yellow-400 hover:bg-yellow-500 text-white px-4 py-2 rounded-xl font-semibold disabled:opacity-50"
// // //           onClick={uploadFiles}
// // //           disabled={loading}
// // //         >
// // //           {loading ? "Uploading..." : "Upload"}
// // //         </button>

// // //         <button
// // //           className="bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded-xl font-semibold"
// // //           onClick={fetchDocs}
// // //         >
// // //           Show Stored Docs
// // //         </button>
// // //       </div>

// // //       {/* Processed documents */}
// // //       {processedDocs.length > 0 && (
// // //         <div className="bg-white p-3 rounded-xl border border-yellow-200 shadow-inner">
// // //           <h3 className="font-semibold text-yellow-700">Stored Documents</h3>
// // //           <ul className="list-disc ml-6 text-gray-700 text-sm mt-2 space-y-1">
// // //             {processedDocs.map(doc => (
// // //               <li key={doc.id}>
// // //                 {doc.filename} — Chunks: {doc.chunks_count}, Embeddings: {doc.embeddings_count}
// // //               </li>
// // //             ))}
// // //           </ul>
// // //         </div>
// // //       )}
// // //     </div>
// // //   );
// // // }

// // "use client";

// // import { useState } from "react";
// // import { getSession } from "next-auth/react";

// // interface FileUploaderProps {
// //   fetchDocs?: () => Promise<void>;
// // }

// // export default function FileUploader({ fetchDocs }: FileUploaderProps) {
// //   const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
// //   const [processedDocs, setProcessedDocs] = useState<any[]>([]);
// //   const [loading, setLoading] = useState(false);
// //   const [showDocsDropdown, setShowDocsDropdown] = useState(false);

// //   const addFiles = (files: FileList | null) => {
// //     if (!files) return;
// //     setSelectedFiles(prev => {
// //       const newFiles = Array.from(files);
// //       const merged = [...prev];
// //       newFiles.forEach(f => {
// //         if (!merged.some(x => x.name === f.name && x.size === f.size)) merged.push(f);
// //       });
// //       return merged;
// //     });
// //   };

// //   const uploadFiles = async () => {
// //     if (selectedFiles.length === 0) return alert("Select files first");
// //     setLoading(true);

// //     const session = await getSession();
// //     const token = (session as any)?.idToken;
// //     if (!token) {
// //       alert("Login first");
// //       setLoading(false);
// //       return;
// //     }

// //     const formData = new FormData();
// //     selectedFiles.forEach(f => formData.append("files", f));

// //     try {
// //       const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/upload`, {
// //         method: "POST",
// //         body: formData,
// //         headers: { Authorization: `Bearer ${token}` },
// //       });
// //       await res.json();
// //       setSelectedFiles([]);
// //       if (fetchDocs) await fetchDocs();
// //       alert("Files uploaded successfully");
// //     } catch (err) {
// //       console.error(err);
// //       alert("Upload failed");
// //     }

// //     setLoading(false);
// //   };

// //   const loaddocs = async () => {
// //     const session = await getSession();
// //     const token = (session as any)?.idToken;
// //     if (!token) return;

// //     const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/docs`, {
// //       headers: { Authorization: `Bearer ${token}` },
// //     });
// //     const data = await res.json();
// //     setProcessedDocs(data);
// //     setShowDocsDropdown(true);
// //   };

// //   return (
// //     <div className="bg-yellow-50 p-4 rounded-xl shadow-md border border-yellow-200 space-y-3">

// //       {/* File input */}
// //       <label className="flex items-center cursor-pointer text-blue-600">
// //         <span className="text-2xl mr-2">+</span> Add files
// //         <input type="file" multiple className="hidden" onChange={e => addFiles(e.target.files)} />
// //       </label>

// //       {/* Selected files */}
// //       {selectedFiles.length > 0 && (
// //         <ul className="list-disc ml-6 text-sm">
// //           {selectedFiles.map((file, i) => (
// //             <li key={i} className="flex justify-between items-center">
// //               {file.name} ({(file.size / 1024).toFixed(1)} KB)
// //               <button
// //                 className="text-red-500 ml-3"
// //                 onClick={() => setSelectedFiles(prev => prev.filter((_, idx) => idx !== i))}
// //               >
// //                 Remove
// //               </button>
// //             </li>
// //           ))}
// //         </ul>
// //       )}

// //       {/* Buttons */}
// //       <div className="flex space-x-2">
// //         <button
// //           className="bg-green-500 text-white px-4 py-2 rounded disabled:opacity-50"
// //           onClick={uploadFiles}
// //           disabled={loading}
// //         >
// //           {loading ? "Uploading..." : "Upload"}
// //         </button>

// //         <button
// //           className="bg-yellow-400 text-white px-4 py-2 rounded"
// //           onClick={loaddocs}
// //         >
// //           Show Stored Docs
// //         </button>
// //       </div>

// //       {/* Dropdown for docs */}
// //       {showDocsDropdown && processedDocs.length > 0 && (
// //         <div className="mt-3 border border-yellow-200 rounded-lg shadow-md bg-white p-3 max-h-60 overflow-y-auto">
// //           <h4 className="font-semibold mb-2 text-yellow-700">📄 Stored Documents</h4>
// //           <table className="table-auto w-full text-left text-sm">
// //             <thead>
// //               <tr className="text-yellow-600 border-b border-yellow-300">
// //                 <th className="px-2 py-1">Filename</th>
// //                 <th className="px-2 py-1">Chunks</th>
// //                 <th className="px-2 py-1">Embeddings</th>
// //               </tr>
// //             </thead>
// //             <tbody>
// //               {processedDocs.map(doc => (
// //                 <tr key={doc.id} className="border-b border-yellow-100 hover:bg-yellow-100 transition">
// //                   <td className="px-2 py-1">{doc.filename}</td>
// //                   <td className="px-2 py-1">{doc.chunks_count}</td>
// //                   <td className="px-2 py-1">{doc.embeddings_count}</td>
// //                 </tr>
// //               ))}
// //             </tbody>
// //           </table>
// //         </div>
// //       )}
// //     </div>
// //   );
// // }

// "use client";

// import { useState } from "react";
// import { getSession } from "next-auth/react";

// export default function FileUploader() {
//   const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
//   const [processedDocs, setProcessedDocs] = useState<any[]>([]);
//   const [loading, setLoading] = useState(false);
//   const [showDocsDropdown, setShowDocsDropdown] = useState(false);

//   const addFiles = (files: FileList | null) => {
//     if (!files) return;
//     setSelectedFiles(prev => {
//       const newFiles = Array.from(files);
//       const merged = [...prev];
//       newFiles.forEach(f => {
//         if (!merged.some(x => x.name === f.name && x.size === f.size)) merged.push(f);
//       });
//       return merged;
//     });
//   };

//   const uploadFiles = async () => {
//     if (selectedFiles.length === 0) return alert("Select files first");
//     setLoading(true);

//     const session = await getSession();
//     const token = (session as any)?.idToken;
//     if (!token) { alert("Login first"); setLoading(false); return; }

//     const formData = new FormData();
//     selectedFiles.forEach(f => formData.append("files", f));

//     try {
//       const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/upload`, {
//         method: "POST",
//         body: formData,
//         headers: { Authorization: `Bearer ${token}` },
//       });
//       await res.json();
//       setSelectedFiles([]);
//       alert("Files uploaded successfully");
//     } catch (err) {
//       console.error(err);
//       alert("Upload failed");
//     }

//     setLoading(false);
//   };

//   const loadDocs = async () => {
//     const session = await getSession();
//     const token = (session as any)?.idToken;
//     if (!token) return;

//     const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/docs`, {
//       headers: { Authorization: `Bearer ${token}` },
//     });
//     const data = await res.json();
//     setProcessedDocs(data);
//     setShowDocsDropdown(prev => !prev); // toggle dropdown
//   };

//   return (
//     <div className="bg-yellow-50 p-4 rounded-xl shadow-md border border-yellow-200 w-80 space-y-4 flex-shrink-0">

//       {/* File Input */}
//       <label className="flex items-center cursor-pointer text-blue-600">
//         <span className="text-2xl mr-2">+</span> Add files
//         <input type="file" multiple className="hidden" onChange={e => addFiles(e.target.files)} />
//       </label>

//       {/* Selected Files */}
//       {selectedFiles.length > 0 && (
//         <ul className="list-disc ml-6 text-sm max-h-40 overflow-y-auto">
//           {selectedFiles.map((file, i) => (
//             <li key={i} className="flex justify-between items-center">
//               {file.name} ({(file.size / 1024).toFixed(1)} KB)
//               <button
//                 className="text-red-500 ml-3"
//                 onClick={() => setSelectedFiles(prev => prev.filter((_, idx) => idx !== i))}
//               >
//                 Remove
//               </button>
//             </li>
//           ))}
//         </ul>
//       )}

//       {/* Buttons */}
//       <div className="flex space-x-2">
//         <button
//           className="bg-green-500 text-white px-4 py-2 rounded disabled:opacity-50"
//           onClick={uploadFiles}
//           disabled={loading}
//         >
//           {loading ? "Uploading..." : "Upload"}
//         </button>
//         <button
//           className="bg-yellow-400 text-white px-4 py-2 rounded"
//           onClick={loadDocs}
//         >
//           {showDocsDropdown ? "Hide Stored Docs" : "Show Stored Docs"}
//         </button>
//       </div>

//       {/* Docs Dropdown */}
//       {showDocsDropdown && processedDocs.length > 0 && (
//         <div className="mt-2 border border-yellow-200 rounded-lg shadow-md bg-white p-3 max-h-60 overflow-y-auto">
//           <h4 className="font-semibold mb-2 text-yellow-700">📄 Stored Documents</h4>
//           <table className="table-auto w-full text-left text-sm">
//             <thead>
//               <tr className="text-yellow-600 border-b border-yellow-300">
//                 <th className="px-2 py-1">Filename</th>
//                 <th className="px-2 py-1">Chunks</th>
//                 <th className="px-2 py-1">Embeddings</th>
//               </tr>
//             </thead>
//             <tbody>
//               {processedDocs.map(doc => (
//                 <tr key={doc.id} className="border-b border-yellow-100 hover:bg-yellow-100 transition">
//                   <td className="px-2 py-1">{doc.filename}</td>
//                   <td className="px-2 py-1">{doc.chunks_count}</td>
//                   <td className="px-2 py-1">{doc.embeddings_count}</td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       )}
//     </div>
//   );
// }

"use client";

import { useState } from "react";
import { getSession } from "next-auth/react";

export default function FileUploader() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [processedDocs, setProcessedDocs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [showDocsDropdown, setShowDocsDropdown] = useState(false);

  const addFiles = (files: FileList | null) => {
    if (!files) return;
    setSelectedFiles(prev => {
      const newFiles = Array.from(files);
      const merged = [...prev];
      newFiles.forEach(f => {
        if (!merged.some(x => x.name === f.name && x.size === f.size)) merged.push(f);
      });
      return merged;
    });
  };

  const uploadFiles = async () => {
    if (selectedFiles.length === 0) return alert("Select files first");
    setLoading(true);

    const session = await getSession();
    const token = (session as any)?.idToken;
    if (!token) { alert("Login first"); setLoading(false); return; }

    const formData = new FormData();
    selectedFiles.forEach(f => formData.append("files", f));

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/upload`, {
        method: "POST",
        body: formData,
        headers: { Authorization: `Bearer ${token}` },
      });
      await res.json();
      setSelectedFiles([]);
      alert("Files uploaded successfully");
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }

    setLoading(false);
  };

  const loadDocs = async () => {
    const session = await getSession();
    const token = (session as any)?.idToken;
    if (!token) return;

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/docs`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await res.json();
    setProcessedDocs(data);
    setShowDocsDropdown(prev => !prev);
  };

  return (
    <div className="bg-yellow-50 p-6 rounded-xl shadow-md border border-yellow-200 w-96 flex-shrink-0 space-y-4">
      <h2 className="text-xl font-semibold text-yellow-700">📁 Your Files</h2>

      {/* File Input */}
      <label className="flex items-center cursor-pointer text-blue-600">
        <span className="text-2xl mr-2">+</span> Add files
        <input type="file" multiple className="hidden" onChange={e => addFiles(e.target.files)} />
      </label>

      {/* Selected Files */}
      {selectedFiles.length > 0 && (
        <ul className="list-disc ml-6 text-sm max-h-40 overflow-y-auto">
          {selectedFiles.map((file, i) => (
            <li key={i} className="flex justify-between items-center">
              {file.name} ({(file.size / 1024).toFixed(1)} KB)
              <button
                className="text-red-500 ml-3"
                onClick={() => setSelectedFiles(prev => prev.filter((_, idx) => idx !== i))}
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}

      {/* Buttons */}
      <div className="flex space-x-2">
        <button
          className="bg-green-500 text-white px-4 py-2 rounded disabled:opacity-50"
          onClick={uploadFiles}
          disabled={loading}
        >
          {loading ? "Uploading..." : "Upload"}
        </button>
        <button
          className="bg-yellow-400 text-white px-4 py-2 rounded"
          onClick={loadDocs}
        >
          {showDocsDropdown ? "Hide Docs" : "Show Docs"}
        </button>
      </div>

      {/* Docs Dropdown */}
      {showDocsDropdown && processedDocs.length > 0 && (
        <div className="mt-2 border border-yellow-200 rounded-lg shadow-md bg-white p-3 max-h-60 overflow-y-auto">
          <h4 className="font-semibold mb-2 text-yellow-700">Stored Documents</h4>
          <table className="table-auto w-full text-left text-sm">
            <thead>
              <tr className="text-yellow-600 border-b border-yellow-300">
                <th className="px-2 py-1">Filename</th>
                <th className="px-2 py-1">Chunks</th>
                <th className="px-2 py-1">Embeddings</th>
              </tr>
            </thead>
            <tbody>
              {processedDocs.map(doc => (
                <tr key={doc.id} className="border-b border-yellow-100 hover:bg-yellow-100 transition">
                  <td className="px-2 py-1">{doc.filename}</td>
                  <td className="px-2 py-1">{doc.chunks_count}</td>
                  <td className="px-2 py-1">{doc.embeddings_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
