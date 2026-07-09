import type { Story } from "./api";

/** Minimal display-language helper: match the story's own language (et/en). */
export function storyLang(story: Story): "et" | "en" {
  return story.language === "et" ? "et" : "en";
}

const FORMAT_LABELS: Record<"et" | "en", Record<string, string>> = {
  en: { song: "song", story: "story", film: "film" },
  et: { song: "laul", story: "lugu", film: "film" },
};

export function recommendationText(story: Story): string {
  const lang = storyLang(story);
  const format = FORMAT_LABELS[lang][story.recommendation.format] ?? story.recommendation.format;
  const reason = story.recommendation.reason[lang];
  return lang === "et"
    ? `See tahab olla ${format} — ${reason}`
    : `This wants to be a ${format} — ${reason}`;
}
