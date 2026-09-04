import type { Story } from "../../lib/api";

/**
 * The one story a stranger sees before signing in. Written to the distill@v2
 * contract (first person, speaker's own images, no closing moral) so the
 * landing promises exactly what the darkroom delivers.
 */
const BASE = {
  id: "sample",
  recommendation: { format: "story", reason: { en: "", et: "" } },
  support_flag: false,
  created_at: "2026-07-09T20:12:00Z",
} as const;

const EN: Story = {
  ...BASE,
  language: "en",
  title: "The Kitchen Radio Was Always On",
  story:
    "My grandmother's kitchen had a radio that was never turned off. Not for the news — she didn't care about the news — but because she said a quiet house sounds like waiting.\n\n" +
    "I would sit on the stool by the window and she would hand me the peeler and not say anything for a long time. The radio talked instead. Somewhere in there she would start humming along, half a beat behind.\n\n" +
    "Last week I caught myself humming in my own kitchen, half a beat behind, and I had to sit down.",
  signature: { tone: "longing", themes: ["grandmother", "kitchen"], people: ["grandmother"] },
};

const ET: Story = {
  ...BASE,
  language: "et",
  title: "Raadio, mida kunagi ei vaigistatud",
  story:
    "Vanaema köögis oli raadio, mida ei pandud kunagi kinni. Mitte uudiste pärast — uudised ei huvitanud teda — vaid sellepärast, et vaikne maja kõlab tema sõnul nagu ootamine.\n\n" +
    "Ma istusin akna all pingil ja ta ulatas mulle kartulikoorija ega öelnud pikka aega midagi. Raadio rääkis meie asemel. Kuskil seal hakkas ta kaasa ümisema, pool lööki hiljem.\n\n" +
    "Eelmisel nädalal tabasin end oma köögis ümisemas, pool lööki hiljem, ja pidin maha istuma.",
  signature: { tone: "longing", themes: ["vanaema", "köök"], people: ["vanaema"] },
};

export function sampleStory(): Story {
  return navigator.language?.toLowerCase().startsWith("et") ? ET : EN;
}
