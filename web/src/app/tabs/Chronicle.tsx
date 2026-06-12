import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, type Story } from "../../lib/api";
import { toneStyle } from "../../lib/signature";

function monthLabel(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, { month: "long", year: "numeric" });
}

export function Chronicle() {
  const [stories, setStories] = useState<Story[] | null>(null);

  useEffect(() => {
    api
      .stories()
      .then((r) => setStories(r.stories))
      .catch(() => setStories([]));
  }, []);

  if (stories === null) {
    return (
      <section className="flex min-h-[50dvh] items-center justify-center">
        <div className="breathe h-2 w-2 rounded-full bg-lamplight-500" aria-label="Loading" />
      </section>
    );
  }

  if (stories.length === 0) {
    return (
      <section className="develop-in px-6 pt-20">
        <p className="text-xs font-medium uppercase tracking-[0.2em] text-ink-500">Chronicle</p>
        <h1 className="mt-6 font-prose text-3xl font-light text-ink-100">
          Your shelves are waiting.
        </h1>
        <p className="mt-4 max-w-xs leading-relaxed text-ink-300">
          Every story you tell is kept here — yours alone, until you choose otherwise.
        </p>
        <Link
          to="/speak"
          className="mt-10 inline-block rounded-full bg-lamplight-500 px-7 py-3 font-ui text-sm font-medium text-night-900"
        >
          Tell the first one
        </Link>
      </section>
    );
  }

  const groups = new Map<string, Story[]>();
  for (const story of stories) {
    const key = monthLabel(story.created_at);
    groups.set(key, [...(groups.get(key) ?? []), story]);
  }

  return (
    <section className="develop-in px-6 pt-20">
      <p className="text-xs font-medium uppercase tracking-[0.2em] text-ink-500">Chronicle</p>

      {[...groups.entries()].map(([month, monthStories]) => (
        <div key={month} className="mt-8">
          <div className="flex items-center gap-3">
            <h2 className="text-sm font-medium text-ink-300">{month}</h2>
            {/* The month's color strip: the chronicle readable at a glance */}
            <div className="flex gap-1" aria-hidden>
              {monthStories.slice(0, 12).map((s) => (
                <span
                  key={s.id}
                  className={`h-2 w-2 rounded-full ${toneStyle(s.signature.tone).text}`}
                  style={{ backgroundColor: "currentcolor" }}
                />
              ))}
            </div>
          </div>

          <ul className="mt-3 space-y-3">
            {monthStories.map((story) => {
              const tone = toneStyle(story.signature.tone);
              return (
                <li key={story.id}>
                  <Link
                    to={`/story/${story.id}`}
                    className={`block rounded-xl border border-night-600 border-l-2 ${tone.border} bg-night-800 p-4 transition-colors duration-150 hover:border-night-500`}
                  >
                    <h3 className="font-prose text-lg font-light text-ink-100">{story.title}</h3>
                    <p className="mt-1 text-xs text-ink-500">
                      <span className={tone.text}>{tone.label}</span>
                      {story.signature.themes.length > 0 && <> · {story.signature.themes.join(", ")}</>}
                    </p>
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </section>
  );
}
