"use client";

import { signIn, useSession } from "next-auth/react";
import { useEffect } from "react";
import { redirect } from "next/navigation";

export default function LoginPage() {
  const { data: session } = useSession();

  useEffect(() => {
    if (session) redirect("/chat");
  }, [session]);

  return (
    <div className="flex flex-col justify-center items-center h-screen bg-gradient-to-b from-yellow-50 to-yellow-200">
      <div className="bg-white p-10 rounded-2xl shadow-lg flex flex-col items-center space-y-6">
        <h1 className="text-3xl font-extrabold text-yellow-600">🍌 Banana-Nana AI</h1>
        <p className="text-gray-700 text-center">
          Login with Google to start chatting with Banana-Nana AI.
        </p>
        <button
          className="bg-yellow-400 hover:bg-yellow-500 text-white px-6 py-3 rounded-xl font-bold shadow-md transition"
          onClick={() => signIn("google", { callbackUrl: "/chat" })}
        >
          Login with Google
        </button>
      </div>
    </div>
  );
}
