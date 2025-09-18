"use client";
import { useState } from "react";

type PlanItem = {
  title: string;
  provider: string;
  level: string;
  why: string;
  estimated_hours: number;
};
type TrainingsResponse = { plan?: PlanItem[]; error?: string };

export default function Trainings() {
  const [loading, setLoading] = useState(false);
  const [out, setOut] = useState<TrainingsResponse | null>(null);

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setOut(null);

    const fd = new FormData(e.currentTarget);
    const body = {
      target_role: String(fd.get("target_role") || ""),
      current_skills: String(fd.get("current_skills") || "")
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean),
      interests: String(fd.get("interests") || "")
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean),
    };

    const r = await fetch("/api/trainings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data: TrainingsResponse = await r.json();
    setOut(data);
    setLoading(false);
  }

  return (
    <main className="mx-auto max-w-5xl p-8 space-y-6">
      <h1 className="text-3xl font-bold">Trainings &amp; Certifications</h1>

      <form onSubmit={submit} className="rounded-2xl border p-6 grid gap-4 sm:grid-cols-2">
        <input name="target_role" className="border rounded-lg p-3 sm:col-span-2" placeholder="Target role" required />
        <input name="current_skills" className="border rounded-lg p-3" placeholder="Current skills (comma-separated)" />
        <input name="interests" className="border rounded-lg p-3" placeholder="Interests (comma-separated)" />
        <div className="sm:col-span-2">
          <button className="rounded-2xl bg-black text-white px-5 py-3" disabled={loading}>
            {loading ? "Recommending…" : "Recommend"}
          </button>
        </div>
      </form>

      {out?.plan && (
        <div className="grid gap-4">
          {out.plan.map((p: PlanItem, i: number) => (
            <div key={`${p.title}-${i}`} className="rounded-2xl border p-6">
              <div className="font-semibold">{p.title}</div>
              <div className="text-sm text-gray-600">
                {p.provider} • {p.level} • ~{p.estimated_hours}h
              </div>
              <p className="mt-2 text-sm">{p.why}</p>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
