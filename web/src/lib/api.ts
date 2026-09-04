import { auth } from "../features/auth/firebase";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

async function authHeader(): Promise<Record<string, string>> {
  const user = auth.currentUser;
  if (!user) throw new ApiError(401, "Not signed in");
  return { Authorization: `Bearer ${await user.getIdToken()}` };
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(`/api${path}`, {
    ...init,
    headers: { ...(init.headers ?? {}), ...(await authHeader()) },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new ApiError(res.status, body.detail ?? res.statusText);
  }
  return res.json() as Promise<T>;
}

export interface Signature {
  tone: "joy" | "bittersweet" | "grief" | "pride" | "calm" | "longing" | "fear" | "wonder";
  themes: string[];
  people: string[];
}

export interface Story {
  id: string;
  title: string;
  story: string;
  language: string;
  signature: Signature;
  recommendation: { format: string; reason: { en: string; et: string } };
  support_flag: boolean;
  created_at: string;
}

export interface EntryStatus {
  entry_id: string;
  status: "distilling" | "done" | "failed";
  story: Story | null;
}

export interface DailyQuestion {
  id: string;
  en: string;
  et: string;
}

export const api = {
  dailyQuestion: () => apiFetch<DailyQuestion>("/daily-question"),
  stories: () => apiFetch<{ stories: Story[] }>("/stories"),
  story: (id: string) => apiFetch<Story>(`/stories/${id}`),
  entry: (id: string) => apiFetch<EntryStatus>(`/entries/${id}`),
  createTextEntry: (text: string) =>
    apiFetch<{ entry_id: string }>("/entries/text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    }),
  /** Erases every entry, recording, story and the sign-in record. Irreversible. */
  deleteAccount: () => apiFetch<{ deleted: Record<string, number> }>("/me", { method: "DELETE" }),
  createAudioEntry: (blob: Blob, durationMs: number) => {
    const form = new FormData();
    form.append("file", blob, "entry");
    form.append("duration_ms", String(Math.round(durationMs)));
    return apiFetch<{ entry_id: string }>("/entries/audio", { method: "POST", body: form });
  },
};
