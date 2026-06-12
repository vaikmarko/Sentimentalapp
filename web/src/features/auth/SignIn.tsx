import { useAuth } from "./AuthProvider";

export function SignIn() {
  const { signInWithGoogle } = useAuth();

  return (
    <main className="flex min-h-dvh flex-col items-center justify-center gap-10 px-8 text-center">
      <div className="develop-in">
        <h1 className="font-prose text-4xl font-light tracking-tight text-ink-100">
          sentimental
        </h1>
        <p className="mt-4 max-w-xs text-base leading-relaxed text-ink-300">
          Talk for two minutes. Get back something beautiful enough to keep,
          share, or gift.
        </p>
      </div>
      <button
        onClick={() => void signInWithGoogle()}
        className="breathe rounded-full bg-lamplight-500 px-8 py-3 font-ui text-sm font-medium text-night-900 transition-transform duration-150 active:scale-95"
      >
        Step into the studio
      </button>
    </main>
  );
}
