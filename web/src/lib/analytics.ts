/**
 * Product analytics: the four funnel events from docs/plan/00 (time-to-magic,
 * keep rate). Sent to Plausible's events API — cookieless, no personal data,
 * no consent banner needed. A no-op unless VITE_PLAUSIBLE_DOMAIN is set, so
 * dev and tests never report.
 */

type EventName = "pageview" | "recording_started" | "story_revealed" | "story_kept";

type Props = Record<string, string | number | boolean>;

const DOMAIN = import.meta.env.VITE_PLAUSIBLE_DOMAIN as string | undefined;
const HOST = (import.meta.env.VITE_PLAUSIBLE_HOST as string | undefined) ?? "https://plausible.io";

function enabled(): boolean {
  if (!DOMAIN || typeof window === "undefined") return false;
  const host = window.location.hostname;
  return host !== "localhost" && host !== "127.0.0.1";
}

export function track(name: EventName, props?: Props): void {
  if (!enabled()) return;
  try {
    void fetch(`${HOST}/api/event`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      keepalive: true,
      body: JSON.stringify({
        name,
        domain: DOMAIN,
        url: window.location.href,
        referrer: document.referrer || undefined,
        props,
      }),
    }).catch(() => undefined);
  } catch {
    // Analytics must never break the product.
  }
}
