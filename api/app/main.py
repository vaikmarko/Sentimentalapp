import logging

import sentry_sdk
from fastapi import FastAPI

from app.core.config import get_settings
from app.routes import demo, entries, health, internal_tasks, stories

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

settings = get_settings()
if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn, environment=settings.environment)

app = FastAPI(
    title="Sentimental API",
    version="0.1.0",
    docs_url="/api/docs" if settings.environment != "production" else None,
)

app.include_router(health.router)
app.include_router(demo.router, prefix="/api")
app.include_router(entries.router, prefix="/api")
app.include_router(stories.router, prefix="/api")
app.include_router(internal_tasks.router)
