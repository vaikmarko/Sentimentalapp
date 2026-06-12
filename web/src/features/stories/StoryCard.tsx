import type { Story } from "../../lib/api";
import { toneStyle } from "../../lib/signature";

/** The artifact surface: editorial serif, Spectrum edge, film-grain feel. */
export function StoryCard({ story, animate = false }: { story: Story; animate?: boolean }) {
  const tone = toneStyle(story.signature.tone);

  return (
    <article
      className={`rounded-2xl border border-night-600 border-l-2 ${tone.border} bg-night-800 p-6 ${
        animate ? "develop-in" : ""
      }`}
    >
      <div className="flex items-center justify-between">
        <span className={`text-xs font-medium uppercase tracking-[0.15em] ${tone.text}`}>
          {tone.label}
        </span>
        {story.signature.themes.length > 0 && (
          <span className="text-xs text-ink-500">{story.signature.themes.join(" · ")}</span>
        )}
      </div>

      <h2 className="mt-4 font-prose text-2xl font-light leading-snug text-ink-100">
        {story.title}
      </h2>

      <div className="mt-5 space-y-4">
        {story.story.split("\n\n").map((paragraph, i) => (
          <p key={i} className="font-prose text-[17px] leading-relaxed text-ink-300">
            {paragraph}
          </p>
        ))}
      </div>

      {story.support_flag && (
        <p className="mt-6 rounded-lg bg-night-700 p-4 text-sm leading-relaxed text-ink-300">
          That sounded heavy. If you need someone to talk to, Eluliin is at{" "}
          <a href="tel:6558088" className="text-lamplight-400">655 8088</a> (Estonia) — or reach
          out to someone you trust.
        </p>
      )}
    </article>
  );
}
