const ENTRIES = [
  {
    title: "Photo spark",
    description: "Pick an old photo. Tell me the story behind it.",
  },
  {
    title: "Make a gift",
    description: "Turn a shared memory into a song or a tale for someone.",
  },
  {
    title: "Free entry",
    description: "No question, no occasion. Just speak.",
  },
] as const;

export function Create() {
  return (
    <section className="develop-in px-6 pt-20">
      <p className="text-xs font-medium uppercase tracking-[0.2em] text-ink-500">
        Create
      </p>
      <h1 className="mt-6 font-prose text-3xl font-light text-ink-100">
        What shall we make?
      </h1>

      <ul className="mt-10 space-y-3">
        {ENTRIES.map(({ title, description }) => (
          <li key={title}>
            <button
              disabled
              className="w-full rounded-xl border border-night-600 bg-night-800 p-5 text-left transition-colors duration-150 hover:border-night-500 disabled:opacity-60"
            >
              <span className="font-prose text-lg text-ink-100">{title}</span>
              <p className="mt-1 text-sm leading-relaxed text-ink-500">{description}</p>
            </button>
          </li>
        ))}
      </ul>
      <p className="mt-6 text-center text-sm text-ink-500">Opening soon.</p>
    </section>
  );
}
