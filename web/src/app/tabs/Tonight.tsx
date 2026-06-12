/**
 * Tonight — the home of the core loop: today's question + the record button.
 * Phase 0 ships the composed surface; recording wires up in Phase 1 (P1.1).
 */
export function Tonight() {
  return (
    <section className="develop-in flex min-h-[calc(100dvh-6rem)] flex-col justify-between px-6 pt-20">
      <header>
        <p className="text-xs font-medium uppercase tracking-[0.2em] text-ink-500">
          Tonight
        </p>
        <h1 className="mt-6 font-prose text-[2rem] font-light leading-snug text-ink-100">
          Tell me about a moment from this year you keep coming back to.
        </h1>
      </header>

      <div className="flex flex-col items-center gap-4 pb-10">
        <button
          aria-label="Start speaking (available soon)"
          disabled
          className="breathe flex h-20 w-20 items-center justify-center rounded-full bg-lamplight-500 text-night-900 shadow-[0_0_40px_-8px] shadow-lamplight-500/60 disabled:opacity-80"
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z" />
            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
            <line x1="12" y1="19" x2="12" y2="22" />
          </svg>
        </button>
        <p className="text-sm text-ink-500">The booth opens soon.</p>
      </div>
    </section>
  );
}
