import { useAuth } from "../../features/auth/AuthProvider";

export function You() {
  const { user, signOut } = useAuth();

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

      <button
        onClick={() => void signOut()}
        className="mt-12 rounded-full border border-night-500 px-6 py-2.5 text-sm font-medium text-ink-300 transition-colors duration-150 hover:border-ink-500 hover:text-ink-100"
      >
        Leave the studio
      </button>
    </section>
  );
}
