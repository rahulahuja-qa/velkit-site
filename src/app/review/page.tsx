import type { Metadata } from "next";
import PageTitle from "../../components/PageTitle";

export const metadata: Metadata = {
  title: "Resume Review · Velkit",
};

export default function Page() {
  return (
    <>
      <PageTitle>Resume Review</PageTitle>
      <main className="mx-auto max-w-5xl p-8">
        <p className="text-gray-600">Coming soon.</p>
      </main>
    </>
  );
}
