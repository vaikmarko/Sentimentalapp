import { useState } from "react";
import { Link } from "react-router-dom";
import { StoryCard } from "../stories/StoryCard";
import { useAuth } from "./AuthProvider";
import { sampleStory } from "./sampleStory";

export function SignIn() {
  const { signInWithGoogle } = useAuth();
  const [error, setError] = useState("");
  const story = sampleStory();
  const et = story.language === "et";

  async function enter() {
    setError("");
    try {
      await signInWithGoogle();
    } catch {
      setError("The door stuck. Try again?");
    }
  }

  return (
    <main className="mx-auto flex min-h-dvh max-w-md flex-col px-6 pb-12 pt-[12vh]">
      <section className="develop-in text-center">
        <h1 className="font-prose text-4xl font-light tracking-tight text-ink-100">sentimental</h1>
        <p className="mx-auto mt-4 max-w-xs text-base leading-relaxed text-ink-300">
          Talk for two minutes. Get back something beautiful enough to keep.
        </p>
        <button
          onClick={() => void enter()}
          className="breathe mt-8 rounded-full bg-lamplight-500 px-8 py-3 font-ui text-sm font-medium text-night-900 transition-transform duration-150 active:scale-95"
        >
          Step into the studio
        </button>
        <p className="mt-3 text-xs text-ink-500">Signs in with Google. Private by default.</p>
        {error && <p className="mt-3 text-sm text-sig-bittersweet">{error}</p>}
      </section>

      <section className="develop-in mt-16" style={{ animationDelay: "300ms" }}>
        <p className="mb-4 text-center text-xs font-medium uppercase tracking-[0.2em] text-ink-500">
          {et ? "Nii näeb üks lugu välja" : "What one looks like"}
        </p>
        <StoryCard story={story} />
        <p className="mt-4 text-center text-xs leading-relaxed text-ink-500">
          {et
            ? "Räägitud kahe minutiga, sõna-sõnalt rääkija oma kujunditest. Midagi juurde ei mõelda."
            : "Spoken in two minutes, kept in the speaker's own images. Nothing is invented."}
        </p>
      </section>

      <footer className="mt-auto pt-16 text-center text-xs text-ink-500">
        <Link to="/privacy" className="underline-offset-4 hover:text-ink-300 hover:underline">
          Privacy
        </Link>
      </footer>
    </main>
  );
}
