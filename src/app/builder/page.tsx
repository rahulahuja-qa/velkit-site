"use client";
import { useState } from "react";

export default function Builder() {
  const [loading, setLoading] = useState(false);
  const [out, setOut] = useState<any>(null);

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true); setOut(null);
    const fd = new FormData(e.currentTarget);
    const body = {
      name: fd.get("name"),
      contact: fd.get("contact"),
      role: fd.get("role"),
      years_exp: Number(fd.get("years_exp") || 0),
      skills: String(fd.get("skills") || "").split(",").map(s=>s.trim()).filter(Boolean),
      job_description: fd.get("job_description"),
    };
    const r = await fetch("/api/builder", {
      method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify(body),
    });
    setOut(await r.json()); setLoading(false);
  }

  return (
    <main className="mx-auto max-w-5xl p-8 space-y-6">
      <h1 className="text-3xl font-bold">Resume &amp; Cover Letter Builder</h1>
      <form onSubmit={submit} className="rounded-2xl border p-6 grid gap-4">
        <input name="name" className="border rounded-lg p-3" placeholder="Your name" required />
        <input name="contact" className="border rounded-lg p-3" placeholder="Contact (email/phone/location)" required />
        <input name="role" className="border rounded-lg p-3" placeholder="Target role" required />
        <input name="years_exp" type="number" min={0} className="border rounded-lg p-3" placeholder="Years of experience" />
        <input name="skills" className="border rounded-lg p-3" placeholder="Key skills (comma-separated)" />
        <textarea name="job_description" className="border rounded-lg p-3 min-h-40" placeholder="Paste job description" required />
        <button className="rounded-2xl bg-black text-white px-5 py-3" disabled={loading}>
          {loading ? "Generating…" : "Generate"}
        </button>
      </form>
      {out && (
        <section className="grid gap-4 sm:grid-cols-2">
          <div className="rounded-2xl border p-6">
            <h2 className="text-lg font-semibold">Cover Letter</h2>
            <pre className="whitespace-pre-wrap text-sm mt-2">
              {out.cover_letter || JSON.stringify(out, null, 2)}
            </pre>
          </div>
          <div className="rounded-2xl border p-6">
            <h2 className="text-lg font-semibold">Resume</h2>
            <pre className="whitespace-pre-wrap text-sm mt-2">
              {JSON.stringify(out.resume || out, null, 2)}
            </pre>
          </div>
        </section>
      )}
    </main>
  );
}
