


import { getSession } from "next-auth/react";

export async function apiPost(path: string, data: any) {
  const session = await getSession()
  const token = (session as any)?.idToken

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { "Authorization": `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(data),
  })
  return res.json()
}

export async function apiGet(path: string) {
  const session = await getSession()
  const token = (session as any)?.idToken

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  return res.json()
}

export interface AskPayload {
  question: string;
  k?: number;
}

export async function askQuestion(payload: AskPayload) {
  return apiPost("/api/ask", payload);
}