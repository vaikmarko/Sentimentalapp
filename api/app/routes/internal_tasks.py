"""Worker routes hit by Cloud Tasks (OIDC-authenticated at the infra layer:
Cloud Run requires authenticated invocations for /internal/*; tasks carry an
OIDC token from the queue's service account)."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.routes.deps import get_runner

router = APIRouter(prefix="/internal/tasks", tags=["internal"])


class StepTask(BaseModel):
    run_id: str


@router.post("/step")
def execute_step(body: StepTask) -> dict:
    get_runner().execute_next_step(body.run_id)
    return {"ok": True}
