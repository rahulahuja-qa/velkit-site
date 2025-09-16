import type { Metadata } from "next";
import PageTitle from "../../components/PageTitle";

export const metadata: Metadata = {
  title: "Trainings & Certifications · Velkit",
};

export default function Page() {
  return (
    <>
      <PageTitle>Trainings & Certifications</PageTitle>
      <main className="mx-auto max-w-5xl p-8">
        <p className="text-gray-600">Coming soon.</p>
      </main>
    </>
  );
}
