# Legacy app — ARCHIVED (2026-07-09)

The legacy Flask app (v1) no longer lives on `main`. It was archived by founder
decision on 2026-07-09; all product work happens in `/web` (React PWA) and
`/api` (FastAPI) per `docs/plan/`.

## Where the code lives

| Ref | Contents |
|---|---|
| branch `legacy-vite-refresh` | **final deployed state** — includes the 2026-07-09 cleanup (api/apps/shared layout, Vite-built frontend, fixed deploy scripts) that is currently running in production |
| tag `legacy-archive-2026-07-09` | last `main` commit that still carried the legacy tree at the repo root (pre-cleanup layout) |

## What is still running (until explicit decommission)

- Cloud Run service `sentimentalapp` (europe-west1, project `sentimental-f95e6`)
  serves the legacy API + app shell at `sentimentalapp.com`.
- Firebase Hosting (root config on the archive branch) serves the static bundle
  and rewrites `/`, `/app`, `/api/**`, `/s/**` to that service.

Deleting the code from `main` does not affect these deployments; they run from
already-built images/releases. To redeploy the legacy app for any reason:

```bash
git checkout legacy-vite-refresh
./deploy/scripts/deploy-production.sh
```

## Decommission checklist (when the traffic flip happens)

1. Point `sentimentalapp.com` hosting at v2 (today v2 lives on the
   `sentimentalapp-test` hosting site; see `deploy/README.md`).
2. Decide the fate of legacy Firestore collections (`stories`, users, uploads) —
   v2 only writes `v2_*` collections; a migration mapping is docs/plan/03 scope.
3. Scale Cloud Run service `sentimentalapp` to zero / delete it.
4. Delete the legacy Firebase Hosting release if the site config moved.

## Data (unchanged)

v2 shares the same Firebase project; new collections are namespaced `v2_*`
(first: `v2_pipeline_runs`). Legacy collections are never written by v2 code
until the migration phase explicitly maps them.
