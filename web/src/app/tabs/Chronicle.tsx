export function Chronicle() {
  return (
    <section className="develop-in px-6 pt-20">
      <p className="text-xs font-medium uppercase tracking-[0.2em] text-ink-500">
        Chronicle
      </p>
      <h1 className="mt-6 font-prose text-3xl font-light text-ink-100">
        Your shelves are waiting.
      </h1>
      <p className="mt-4 max-w-xs leading-relaxed text-ink-300">
        Every story you tell is kept here — yours alone, until you choose
        otherwise.
      </p>

      <div className="mt-12 space-y-3" aria-hidden>
        {/* Placeholder shelf: the empty state hints at what will live here */}
        <div className="h-16 rounded-xl border border-night-600 border-l-2 border-l-sig-joy bg-night-800 opacity-50" />
        <div className="h-16 rounded-xl border border-night-600 border-l-2 border-l-sig-calm bg-night-800 opacity-50" />
        <div className="h-16 rounded-xl border border-night-600 border-l-2 border-l-sig-bittersweet bg-night-800 opacity-50" />
      </div>
    </section>
  );
}
