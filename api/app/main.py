import logging

import sentry_sdk
from fastapi import FastAPI

from app.core.config import get_settings
from app.routes import account, entries, health, internal_tasks, stories

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

settings = get_settings()
if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn, environment=settings.environment)

if settings.environment == "production" and settings.fake_providers:
    # Refuse to serve the canned "rice she always burned" story to real people.
    raise RuntimeError(
        "FAKE_PROVIDERS=true in production — OPENAI_API_KEY is missing from the deploy."
    )

app = FastAPI(
    title="Sentimental API",
    version="0.1.0",
    docs_url="/api/docs" if settings.environment != "production" else None,
)

app.include_router(health.router)
app.include_router(entries.router, prefix="/api")
app.include_router(stories.router, prefix="/api")
app.include_router(account.router, prefix="/api")
if not settings.tasks_inline:
    # Only expose the worker surface when something actually enqueues to it.
    app.include_router(internal_tasks.router)
