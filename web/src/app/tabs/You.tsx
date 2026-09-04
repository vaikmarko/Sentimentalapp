import { useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../features/auth/AuthProvider";
import { api } from "../../lib/api";

type DeleteState = "idle" | "confirm" | "working" | "error";

export function You() {
  const { user, signOut } = useAuth();
  const [del, setDel] = useState<DeleteState>("idle");

  async function deleteEverything() {
    setDel("working");
    try {
      await api.deleteAccount();
      await signOut();
    } catch {
      setDel("error");
    }
  }

  return (
    <section className="develop-in px-6 pt-20">
      <p className="text-xs font-medium uppercase tracking-[0.2em] text-ink-500">
        You
      </p>
      <h1 className="mt-6 font-prose text-3xl font-light text-ink-100">
        {user?.displayName ?? "Storyteller"}
      </h1>
      <p className="mt-4 max-w-xs leading-relaxed text-ink-300">
        Your reflections are yours. Only what you choose to publish leaves the
        vault.
      </p>
      <Link
        to="/privacy"
        className="mt-3 inline-block text-sm text-ink-500 underline-offset-4 hover:text-ink-300 hover:underline"
      >
        What we keep, and why
      </Link>

      <button
        onClick={() => void signOut()}
        className="mt-12 block rounded-full border border-night-500 px-6 py-2.5 text-sm font-medium text-ink-300 transition-colors duration-150 hover:border-ink-500 hover:text-ink-100"
      >
        Leave the studio
      </button>

      <div className="mt-16 border-t border-night-600 pt-8">
        {del === "idle" && (
          <button
            onClick={() => setDel("confirm")}
            className="text-sm text-ink-500 underline-offset-4 hover:text-sig-bittersweet hover:underline"
          >
            Delete my account and everything in it
          </button>
        )}

        {(del === "confirm" || del === "error") && (
          <div className="rounded-xl border border-night-600 bg-night-800 p-5">
            <p className="font-prose text-lg font-light text-ink-100">
              This empties the shelves for good.
            </p>
            <p className="mt-2 text-sm leading-relaxed text-ink-300">
              Every recording, transcript and story is erased, and your sign-in is
              removed. There is no undo and no copy kept.
            </p>
            {del === "error" && (
              <p className="mt-3 text-sm text-sig-bittersweet">
                That didn't go through. Try again, or write to us from the privacy page.
              </p>
            )}
            <div className="mt-5 flex gap-3">
              <button
                onClick={() => setDel("idle")}
                className="flex-1 rounded-full border border-night-500 py-2.5 text-sm text-ink-300"
              >
                Keep them
              </button>
              <button
                onClick={() => void deleteEverything()}
                className="flex-1 rounded-full bg-sig-bittersweet/90 py-2.5 text-sm font-medium text-night-900"
              >
                Delete everything
              </button>
            </div>
          </div>
        )}

        {del === "working" && (
          <p className="text-sm text-ink-500" aria-live="polite">
            Clearing the shelves…
          </p>
        )}
      </div>
    </section>
  );
}
