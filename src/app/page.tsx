import Link from "next/link";

export default function Home() {
  return (
    <main className="mx-auto max-w-5xl p-8">
      <div className="grid gap-4 sm:grid-cols-3">
        <Link
          href="/builder"
          className="rounded-xl border p-6 hover:shadow-md focus:outline-none focus:ring-2"
        >
          <h2 className="text-lg font-semibold">Resume & Cover Letter Builder</h2>
          <p className="mt-1 text-sm text-gray-600">Generate tailored drafts.</p>
        </Link>

        <Link
          href="/review"
          className="rounded-xl border p-6 hover:shadow-md focus:outline-none focus:ring-2"
        >
          <h2 className="text-lg font-semibold">Resume Review</h2>
          <p className="mt-1 text-sm text-gray-600">Get structured feedback.</p>
        </Link>

        <Link
          href="/trainings"
          className="rounded-xl border p-6 hover:shadow-md focus:outline-none focus:ring-2"
        >
          <h2 className="text-lg font-semibold">Trainings & Certifications</h2>
          <p className="mt-1 text-sm text-gray-600">Recommendations by role.</p>
        </Link>
      </div>
    </main>
  );
}
