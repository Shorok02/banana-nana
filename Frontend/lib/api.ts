export async function apiGet(path: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`);
  return res.json();
}

export async function apiPost(path: string, data: any) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export interface AskPayload {
  question: string;
  k?: number;
}

export async function askQuestion(payload: AskPayload) {
  return apiPost("/api/ask", payload);
}
