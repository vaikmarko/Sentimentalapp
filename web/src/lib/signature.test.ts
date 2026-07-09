import { describe, expect, it } from "vitest";
import { TONE_STYLES, toneStyle } from "./signature";

describe("signature spectrum", () => {
  it("covers all eight tones", () => {
    expect(Object.keys(TONE_STYLES)).toHaveLength(8);
  });

  it("falls back to calm for unknown tones", () => {
    // @ts-expect-error deliberately invalid tone
    expect(toneStyle("unknown")).toBe(TONE_STYLES.calm);
  });

  it("every tone has border, text and label", () => {
    for (const style of Object.values(TONE_STYLES)) {
      expect(style.border).toMatch(/^border-l-sig-/);
      expect(style.text).toMatch(/^text-sig-/);
      expect(style.label.length).toBeGreaterThan(0);
    }
  });
});
