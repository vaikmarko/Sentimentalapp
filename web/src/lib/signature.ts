import type { Signature } from "./api";

/** Signature Spectrum mapping (docs/plan/02): tone -> token classes + label. */
export const TONE_STYLES: Record<
  Signature["tone"],
  { border: string; text: string; label: string }
> = {
  joy: { border: "border-l-sig-joy", text: "text-sig-joy", label: "joy" },
  bittersweet: { border: "border-l-sig-bittersweet", text: "text-sig-bittersweet", label: "bittersweet" },
  grief: { border: "border-l-sig-grief", text: "text-sig-grief", label: "grief" },
  pride: { border: "border-l-sig-pride", text: "text-sig-pride", label: "pride" },
  calm: { border: "border-l-sig-calm", text: "text-sig-calm", label: "calm" },
  longing: { border: "border-l-sig-longing", text: "text-sig-longing", label: "longing" },
  fear: { border: "border-l-sig-fear", text: "text-sig-fear", label: "fear" },
  wonder: { border: "border-l-sig-wonder", text: "text-sig-wonder", label: "wonder" },
};

export function toneStyle(tone: Signature["tone"]) {
  return TONE_STYLES[tone] ?? TONE_STYLES.calm;
}
