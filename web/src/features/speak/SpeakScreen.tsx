import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { capabilities } from "../../capabilities";
import { api } from "../../lib/api";
import { track } from "../../lib/analytics";
import { Waveform } from "./Waveform";

const SILENCE_LEVEL = 0.06;
const NUDGE_AFTER_MS = 8_000;
const MAX_DURATION_MS = 5 * 60_000;

const MICRO_PROMPTS = [
  "What happened next?",
  "How did that feel?",
  "Who else was there?",
  "What do you remember most clearly?",
];

type Mode = "idle" | "recording" | "uploading" | "typing" | "error";

export function SpeakScreen() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<Mode>("idle");
  const [level, setLevel] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const [nudge, setNudge] = useState<string | null>(null);
  const [text, setText] = useState("");
  const [error, setError] = useState("");

  const lastVoiceAt = useRef(Date.now());
  const startedAt = useRef(0);
  const nudgeIndex = useRef(0);

  const onLevel = useCallback((v: number) => {
    setLevel(v);
    if (v > SILENCE_LEVEL) {
      lastVoiceAt.current = Date.now();
      setNudge(null);
    }
  }, []);

  // Elapsed timer + silence nudges + max-duration stop.
  useEffect(() => {
    if (mode !== "recording") return;
    const interval = window.setInterval(() => {
      const now = Date.now();
      setElapsed(now - startedAt.current);
      if (now - lastVoiceAt.current > NUDGE_AFTER_MS) {
        setNudge(MICRO_PROMPTS[nudgeIndex.current % MICRO_PROMPTS.length]);
        nudgeIndex.current += 1;
        lastVoiceAt.current = now; // don't repeat every tick
      }
      if (now - startedAt.current > MAX_DURATION_MS) void finish();
    }, 500);
    return () => window.clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode]);

  async function start() {
    try {
      await capabilities.mic.start(onLevel);
      startedAt.current = Date.now();
      lastVoiceAt.current = Date.now();
      setElapsed(0);
      setMode("recording");
      track("recording_started", { source: "voice" });
    } catch {
      startTyping(); // mic denied/unavailable -> graceful text fallback
    }
  }

  function startTyping() {
    setMode("typing");
    track("recording_started", { source: "text" });
  }

  async function finish() {
    setMode("uploading");
    try {
      const rec = await capabilities.mic.stop();
      if (rec.durationMs < 3_000) {
        setError("That was a very short one — try again?");
        setMode("idle");
        return;
      }
      const { entry_id } = await api.createAudioEntry(rec.blob, rec.durationMs);
      capabilities.haptics.tap();
      navigate(`/entry/${entry_id}`, { replace: true });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
      setMode("error");
    }
  }

  async function submitText() {
    setMode("uploading");
    try {
      const { entry_id } = await api.createTextEntry(text.trim());
      navigate(`/entry/${entry_id}`, { replace: true });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
      setMode("error");
    }
  }

  function cancel() {
    if (mode === "recording") capabilities.mic.cancel();
    navigate(-1);
  }

  const mins = Math.floor(elapsed / 60_000);
  const secs = Math.floor((elapsed % 60_000) / 1000);

  return (
    <main className="flex min-h-dvh flex-col bg-night-900 px-6">
      <header className="flex items-center justify-between pt-6">
        <button onClick={cancel} className="p-2 text-ink-500 hover:text-ink-300" aria-label="Close">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" aria-hidden>
            <path d="M18 6 6 18M6 6l12 12" />
          </svg>
        </button>
        {mode === "recording" && (
          <span className="font-ui text-sm tabular-nums text-ink-300" aria-live="polite">
            {mins}:{secs.toString().padStart(2, "0")}
          </span>
        )}
      </header>

      {mode === "typing" ? (
        <section className="develop-in flex flex-1 flex-col pt-10">
          <h1 className="font-prose text-2xl font-light text-ink-100">Write it instead.</h1>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            autoFocus
            placeholder="Start anywhere. The middle is fine."
            className="mt-6 flex-1 resize-none rounded-xl border border-night-600 bg-night-800 p-4 font-prose text-lg leading-relaxed text-ink-100 placeholder:text-ink-500 focus:border-dusk-500 focus:outline-none"
          />
          <button
            onClick={() => void submitText()}
            disabled={text.trim().length < 20}
            className="mb-8 mt-4 rounded-full bg-lamplight-500 py-3.5 font-ui text-sm font-medium text-night-900 disabled:opacity-40"
          >
            Develop the story
          </button>
        </section>
      ) : (
        <section className="flex flex-1 flex-col items-center justify-between pb-12 pt-16 text-center">
          <div className="develop-in" aria-live="polite">
            {mode === "recording" ? (
              <p className="font-prose text-xl font-light text-ink-300">
                {nudge ?? "I'm listening."}
              </p>
            ) : mode === "uploading" ? (
              <p className="font-prose text-xl font-light text-dusk-300">
                Taking it to the darkroom…
              </p>
            ) : (
              <p className="font-prose text-xl font-light text-ink-100">
                Just talk. I'll do the rest.
              </p>
            )}
            {error && <p className="mt-3 text-sm text-sig-bittersweet">{error}</p>}
          </div>

          {mode === "recording" && <Waveform level={level} />}

          <div className="flex flex-col items-center gap-5">
            {mode === "recording" ? (
              <button
                onClick={() => void finish()}
                aria-label="Finish recording"
                className="flex h-20 w-20 items-center justify-center rounded-full border-2 border-lamplight-500 text-lamplight-400 shadow-[0_0_50px_-10px] shadow-lamplight-500/70"
              >
                <span className="block h-6 w-6 rounded bg-lamplight-500" />
              </button>
            ) : mode === "uploading" ? (
              <div className="breathe h-20 w-20 rounded-full bg-dusk-500/30" aria-label="Uploading" />
            ) : (
              <button
                onClick={() => void start()}
                aria-label="Start recording"
                className="breathe flex h-20 w-20 items-center justify-center rounded-full bg-lamplight-500 text-night-900 shadow-[0_0_50px_-10px] shadow-lamplight-500/70"
              >
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
                  <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z" />
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                  <line x1="12" y1="19" x2="12" y2="22" />
                </svg>
              </button>
            )}
            {mode === "idle" && (
              <button onClick={startTyping} className="text-sm text-ink-500 underline-offset-4 hover:text-ink-300 hover:underline">
                write instead
              </button>
            )}
          </div>
        </section>
      )}
    </main>
  );
}
