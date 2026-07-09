import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api, type EntryStatus } from "../../lib/api";
import { capabilities } from "../../capabilities";
import { recommendationText } from "../../lib/i18n";
import { StoryCard } from "../stories/StoryCard";

const POLL_MS = 1500;

export function RevealScreen() {
  const { entryId } = useParams<{ entryId: string }>();
  const navigate = useNavigate();
  const [entry, setEntry] = useState<EntryStatus | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    if (!entryId) return;
    let cancelled = false;
    let timer: number;

    const poll = async () => {
      try {
        const next = await api.entry(entryId);
        if (cancelled) return;
        setEntry(next);
        if (next.status === "distilling") {
          timer = window.setTimeout(() => void poll(), POLL_MS);
        } else if (next.status === "done") {
          capabilities.haptics.tap();
        } else {
          setFailed(true);
        }
      } catch {
        if (!cancelled) setFailed(true);
      }
    };
    void poll();
    return () => {
      cancelled = true;
      window.clearTimeout(timer);
    };
  }, [entryId]);

  if (failed) {
    return (
      <main className="flex min-h-dvh flex-col items-center justify-center gap-6 px-8 text-center">
        <p className="font-prose text-xl font-light text-ink-100">
          The darkroom hiccuped — your words are safe, but the story didn't
          develop this time.
        </p>
        <button
          onClick={() => navigate("/", { replace: true })}
          className="rounded-full border border-night-500 px-6 py-2.5 text-sm text-ink-300"
        >
          Back to tonight
        </button>
      </main>
    );
  }

  if (!entry || entry.status === "distilling" || !entry.story) {
    return (
      <main className="flex min-h-dvh flex-col items-center justify-center gap-8 px-8 text-center">
        <div className="breathe h-16 w-16 rounded-full bg-dusk-500/25 shadow-[0_0_60px_-10px] shadow-dusk-500/60" aria-hidden />
        <p className="font-prose text-xl font-light text-dusk-300" aria-live="polite">
          Developing your story…
        </p>
      </main>
    );
  }

  const story = entry.story;
  return (
    <main className="mx-auto min-h-dvh max-w-md px-5 pb-12 pt-10">
      <StoryCard story={story} animate />

      <div className="develop-in mt-6 space-y-4" style={{ animationDelay: "400ms" }}>
        <div className="rounded-xl border border-dusk-600/40 bg-dusk-600/10 p-4">
          <p className="text-sm leading-relaxed text-dusk-300">
            <span className="font-medium">{recommendationText(story)}</span>{" "}
            <span className="text-ink-500">(coming in the next phase)</span>
          </p>
        </div>

        <div className="flex gap-3">
          <Link
            to="/chronicle"
            className="flex-1 rounded-full bg-lamplight-500 py-3 text-center font-ui text-sm font-medium text-night-900"
          >
            Keep
          </Link>
          <button disabled className="flex-1 rounded-full border border-night-500 py-3 text-sm text-ink-500" title="Coming soon">
            Share
          </button>
          <button disabled className="flex-1 rounded-full border border-night-500 py-3 text-sm text-ink-500" title="Coming soon">
            Gift
          </button>
        </div>
      </div>
    </main>
  );
}
