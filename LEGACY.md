# Legacy app — ARCHIVED (2026-07-09)

The legacy Flask app (v1) no longer lives on `main`. It was archived by founder
decision on 2026-07-09; all product work happens in `/web` (React PWA) and
`/api` (FastAPI) per `docs/plan/`.

## Where the code lives

| Ref | Contents |
|---|---|
| branch `legacy-vite-refresh` | **final deployed state** — includes the 2026-07-09 cleanup (api/apps/shared layout, Vite-built frontend, fixed deploy scripts) that is currently running in production |
| tag `legacy-archive-2026-07-09` | last `main` commit that still carried the legacy tree at the repo root (pre-cleanup layout) |

## Traffic flip — DONE (2026-07-09)

The legacy app had no real users (mock/demo accounts only), so the strangler
migration's traffic flip happened immediately after archiving:

- `sentimentalapp.com` (Firebase Hosting site `sentimental-f95e6`, target
  `production` in `deploy/`) now serves the **v2** web build with `/api/**`
  rewritten to Cloud Run `sentimental-api-v2`.
- `sentimentalapp-test.web.app` remains as the staging site (same build).

To redeploy the legacy app for any reason:

```bash
git checkout legacy-vite-refresh
./deploy/scripts/deploy-production.sh   # NB: would re-point hosting back to legacy
```

## Remaining decommission items

1. Legacy Cloud Run services in project `sentimental-f95e6` are still deployed
   but receive no traffic (idle = ~zero cost): `sentimentalapp` (ew + uc),
   `sentimentalapp-eu`, `sentimentalapp-prod`, `sentimentalapp-test`,
   `sentimental-app`. Delete when confident.
2. Legacy Firestore collections (`stories`, users, uploads) still exist;
   v2 only writes `v2_*` collections. Purge or migrate explicitly.

## Data (unchanged)

v2 shares the same Firebase project; new collections are namespaced `v2_*`
(first: `v2_pipeline_runs`). Legacy collections are never written by v2 code
until the migration phase explicitly maps them.
