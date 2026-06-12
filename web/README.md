# Sentimental Web (v2)

The single React PWA replacing the legacy duplicate bundles
(`static/js/sentimental-app.jsx` + `public/static/js/sentimental-app.jsx`).
Design system and decisions: see `docs/plan/02` and `docs/plan/03`.

## Stack

React 18 + TypeScript (strict) + Vite + Tailwind v4 + `vite-plugin-pwa`.
Firebase Auth (Google sign-in). API calls proxy to `/api` (FastAPI service).

## Commands

```bash
npm install
npm run dev        # dev server at :5173, /api proxied to :8000
npm run typecheck
npm run test
npm run build      # production build in dist/
```

## Structure

```
src/design/        tokens.css — Night Studio theme (single source of truth)
src/app/           shell + 5 tab routes (Tonight, Chronicle, Create, Resonance, You)
src/features/      auth (more features land per docs/plan/05 phases)
src/capabilities/  Mic/Push/Share/Haptics interfaces + web implementations;
                   Capacitor implementations arrive in Phase B behind the same types
```

## Environment

Public Firebase web config can be overridden via `VITE_FIREBASE_*` env vars
(defaults target the `sentimental-f95e6` project; these values are public
identifiers, not secrets).
