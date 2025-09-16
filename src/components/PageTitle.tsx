export default function PageTitle({ children }: { children: React.ReactNode }) {
  return (
    <div className="border-b bg-gray-50">
      <div className="mx-auto max-w-5xl p-4">
        <h1 className="text-xl font-semibold">{children}</h1>
      </div>
    </div>
  );
}
