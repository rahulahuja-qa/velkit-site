export default function Home() {
  return (
    <main className="mx-auto max-w-3xl p-8 text-center">
      <h1 className="text-4xl font-bold">Welcome to Velkit</h1>
      <p className="mt-4 text-gray-600">
        AI-powered solutions. No data stored. Just instant results.
      </p>
      <a
        href="mailto:hello@velkit.io"
        className="mt-6 inline-block rounded bg-black px-6 py-3 text-white"
      >
        Contact Us
      </a>
    </main>
  );
}
