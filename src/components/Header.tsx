import Image from "next/image";
import Link from "next/link";

export default function Header() {
  return (
    <header className="border-b">
      <div className="mx-auto max-w-5xl p-4 flex items-center gap-3">
        <Link href="/" className="flex items-center gap-2">
          <Image src="/velkit-logo.png" alt="Velkit" width={108} height={108} priority />
        </Link>
        <nav className="ml-auto">
          <a href="mailto:hello@velkit.io" className="rounded bg-black px-3 py-1 text-white">
            Contact
          </a>
        </nav>
      </div>
    </header>
  );
}
