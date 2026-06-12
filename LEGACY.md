# Legacy freeze (Phase 0, F0.4)

The Flask app at the repo root (`app.py` + engines + `static/`/`public/`
bundles + `templates/`) is **frozen**: it keeps serving existing users and
deploys unchanged, but receives no new features. All new work happens in
`/web` (React PWA) and `/api` (FastAPI) per `docs/plan/03`.

The physical move to a `/legacy` directory is deliberately deferred to the
traffic-flip moment (end of the strangler migration): moving now would break
the root-based deploy flows (`gcloud run deploy --source .`, root `Dockerfile`,
`firebase.json` pointing at `public/`) for no user-facing benefit.

## Deployment (unchanged)

See `README.md` and `SIMPLE_DEPLOYMENT.md`. Cloud Run service deploys from the
repo root; Firebase Hosting serves `public/` with `/s/**` rewritten to Cloud Run.

## Route inventory (frozen surface)

Pages: `/`, `/app`, `/landing`, `/manifest.json`, `/cosmos`, `/chat`, `/deck`,
`/story`, `/inner-space`, `/debug`, `/static/uploads/<file>`,
`/s/<story_id>[/<format_type>]` (public share pages — concept carries into v2).

Stories API: CRUD on `/api/stories[...]`, likes/reactions/comments,
`/api/stories/<id>/formats/<type>` (GET/PUT), `/api/stories/<id>/generate-format`,
`/api/stories/generate`, `/api/stories/<id>/privacy`,
`/api/users/<id>/generate-book-chapter`, `/api/connections/<id>`,
`/api/insights/<id>`.

Chat: `/api/chat/message`.

Auth: `/api/auth/register|login|firebase-signup|firebase-signin|firebase-sync|
check-access-code|verify-user-access|fix-marko-user`.

Uploads: `/api/upload/audio` (the MP3 path the v2 Studio queue will reuse,
see docs/plan/07), `/api/upload/image`.

Misc/admin/debug: `/api/ai/providers`, `/api/formats/supported`,
`/api/admin/*`, `/api/debug/*`.

MentalOS (parked product, see docs/plan/00): `/api/mental-os/*`.

## Data

v2 shares the same Firebase project; new collections are namespaced `v2_*`
(first: `v2_pipeline_runs`). Legacy collections are never written by v2 code
until the migration phase explicitly maps them.
