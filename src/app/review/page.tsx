"use client";
import { useState } from "react";

export default function Review() {
  const [loading, setLoading] = useState(false);
  const [out, setOut] = useState<any>(null);

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true); setOut(null);
    const fd = new FormData(e.currentTarget);
    const r = await fetch("/api/review", { method: "POST", body: fd });
    setOut(await r.json()); setLoading(false);
  }

  return (
    <main className="mx-auto max-w-5xl p-8 space-y-6">
      <h1 className="text-3xl font-bold">Resume Review</h1>
      <form onSubmit={submit} className="rounded-2xl border p-6 grid gap-4">
        <input type="file" name="resume" accept=".pdf,.docx,.txt" className="border rounded-lg p-3" required />
        <textarea name="job_description" className="border rounded-lg p-3 min-h-40" placeholder="Paste job description" required />
        <button className="rounded-2xl bg-black text-white px-5 py-3" disabled={loading}>
          {loading ? "Reviewing…" : "Review"}
        </button>
      </form>
      {out && (
        <section className="grid gap-4">
          <div className="rounded-2xl border p-6">
            <h2 className="text-lg font-semibold">ATS Score</h2>
            <p className="text-2xl mt-1">{out.ats_score ?? "-"}</p>
          </div>
          <div className="rounded-2xl border p-6">
            <h2 className="text-lg font-semibold">Missing Keywords</h2>
            <ul className="list-disc pl-6 mt-2">
              {(out.missing_keywords || []).map((k: string) => <li key={k}>{k}</li>)}
            </ul>
          </div>
          <div className="rounded-2xl border p-6">
            <h2 className="text-lg font-semibold">Rewrite Suggestions</h2>
            <ul className="list-disc pl-6 mt-2">
              {(out.rewrite_suggestions || []).map((s: string, i: number) => <li key={i}>{s}</li>)}
            </ul>
          </div>
        </section>
      )}
    </main>
  );
}
