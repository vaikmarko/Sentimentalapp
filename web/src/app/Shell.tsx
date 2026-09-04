import { NavLink, Outlet } from "react-router-dom";

// Only surfaces that actually work are shown. Create and Resonance return as
// tabs when their features ship (docs/plan/05) — never as "coming soon" stubs.
const TABS = [
  { to: "/", label: "Tonight", icon: MoonIcon },
  { to: "/chronicle", label: "Chronicle", icon: BookIcon },
  { to: "/you", label: "You", icon: PersonIcon },
] as const;

export function Shell() {
  return (
    <div className="mx-auto flex min-h-dvh max-w-md flex-col">
      <main className="flex-1 pb-24">
        <Outlet />
      </main>
      <nav
        aria-label="Main"
        className="fixed inset-x-0 bottom-0 mx-auto max-w-md border-t border-night-600 bg-night-800/90 pb-[env(safe-area-inset-bottom)] backdrop-blur"
      >
        <ul className="flex items-stretch justify-around">
          {TABS.map(({ to, label, icon: Icon }) => (
            <li key={to} className="flex-1">
              <NavLink
                to={to}
                end={to === "/"}
                className={({ isActive }) =>
                  `flex flex-col items-center gap-1 py-3 text-[11px] font-medium transition-colors duration-150 ${
                    isActive ? "text-lamplight-400" : "text-ink-500 hover:text-ink-300"
                  }`
                }
              >
                <Icon />
                {label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}

function MoonIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
    </svg>
  );
}

function BookIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
    </svg>
  );
}

function PersonIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  );
}
