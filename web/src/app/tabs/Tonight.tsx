import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, type DailyQuestion, type Story } from "../../lib/api";

function pickLanguage(q: DailyQuestion): string {
  return navigator.language?.toLowerCase().startsWith("et") ? q.et : q.en;
}

export function Tonight() {
  const [question, setQuestion] = useState<DailyQuestion | null>(null);
  const [latest, setLatest] = useState<Story | null>(null);

  useEffect(() => {
    api.dailyQuestion().then(setQuestion).catch(() => null);
    api
      .stories()
      .then((r) => setLatest(r.stories[0] ?? null))
      .catch(() => null);
  }, []);

  return (
    <section className="develop-in flex min-h-[calc(100dvh-6rem)] flex-col justify-between px-6 pt-20">
      <header>
        <p className="text-xs font-medium uppercase tracking-[0.2em] text-ink-500">Tonight</p>
        <h1 className="mt-6 font-prose text-[2rem] font-light leading-snug text-ink-100">
          {question ? pickLanguage(question) : "\u00a0"}
        </h1>
      </header>

      <div className="flex flex-col items-center gap-6 pb-8">
        <Link
          to="/speak"
          aria-label="Start speaking"
          className="breathe flex h-20 w-20 items-center justify-center rounded-full bg-lamplight-500 text-night-900 shadow-[0_0_40px_-8px] shadow-lamplight-500/60 transition-transform duration-150 active:scale-95"
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z" />
            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
            <line x1="12" y1="19" x2="12" y2="22" />
          </svg>
        </Link>

        {latest && (
          <Link
            to={`/story/${latest.id}`}
            className="w-full rounded-xl border border-night-600 bg-night-800/70 p-4 text-left"
          >
            <p className="text-xs text-ink-500">Last from the shelf</p>
            <p className="mt-1 font-prose text-base text-ink-300">{latest.title}</p>
          </Link>
        )}
      </div>
    </section>
  );
}
