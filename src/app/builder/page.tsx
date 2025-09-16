import type { Metadata } from "next";
import PageTitle from "../../components/PageTitle";

export const metadata: Metadata = {
  title: "Resume & Cover Letter Builder · Velkit",
};

export default function Page() {
  return (
    <>
      <PageTitle>Resume & Cover Letter Builder</PageTitle>
      <main className="mx-auto max-w-5xl p-8">
        <p className="text-gray-600">Coming soon.</p>
      </main>
    </>
  );
}
