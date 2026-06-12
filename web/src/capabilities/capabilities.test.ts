import { describe, expect, it, vi } from "vitest";
import { capabilities } from "./index";

describe("capabilities layer", () => {
  it("exposes all four capability surfaces", () => {
    expect(capabilities.mic).toBeDefined();
    expect(capabilities.push).toBeDefined();
    expect(capabilities.share).toBeDefined();
    expect(capabilities.haptics).toBeDefined();
  });

  it("mic reports unavailable when MediaRecorder is missing (jsdom)", async () => {
    await expect(capabilities.mic.isAvailable()).resolves.toBe(false);
  });

  it("share falls back to clipboard when navigator.share is missing", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.assign(navigator, { clipboard: { writeText } });
    const ok = await capabilities.share.share({ url: "https://example.com/s/x" });
    expect(ok).toBe(true);
    expect(writeText).toHaveBeenCalledWith("https://example.com/s/x");
  });

  it("haptics tap is a safe no-op without vibration support", () => {
    expect(() => capabilities.haptics.tap()).not.toThrow();
  });
});
