import type { Capabilities, PushCapability, ShareCapability, HapticsCapability, SharePayload } from "./types";
import { WebMic } from "./mic.web";

const webPush: PushCapability = {
  async isAvailable() {
    return "Notification" in window && "serviceWorker" in navigator;
  },
  async requestPermission() {
    if (!("Notification" in window)) return "denied";
    return Notification.requestPermission();
  },
};

const webShare: ShareCapability = {
  isAvailable() {
    return typeof navigator.share === "function";
  },
  async share(payload: SharePayload) {
    if (typeof navigator.share === "function") {
      try {
        await navigator.share(payload);
        return true;
      } catch {
        return false; // user cancelled or share failed
      }
    }
    await navigator.clipboard.writeText(payload.url);
    return true;
  },
};

const webHaptics: HapticsCapability = {
  tap() {
    navigator.vibrate?.(10);
  },
};

export const capabilities: Capabilities = {
  mic: new WebMic(),
  push: webPush,
  share: webShare,
  haptics: webHaptics,
};

export type { Capabilities } from "./types";
