"""Worker route hit by Cloud Tasks.

The Cloud Run service is public (the web app calls /api/* directly), so this
route verifies the task's OIDC token itself: it must be a Google-signed ID
token for this exact URL, issued to the queue's service account. The router is
only mounted when TASKS_INLINE=false (see app.main), so in inline mode there is
no unauthenticated surface at all.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from app.core.config import get_settings
from app.routes.deps import get_runner

router = APIRouter(prefix="/internal/tasks", tags=["internal"])


def task_service_account() -> str:
    return f"{get_settings().gcp_project}@appspot.gserviceaccount.com"


def step_url() -> str:
    return f"{get_settings().worker_base_url}/internal/tasks/step"


def verify_task_token(request: Request) -> None:
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing task token")
    token = header.removeprefix("Bearer ").strip()

    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token

    try:
        claims = id_token.verify_oauth2_token(token, google_requests.Request(), audience=step_url())
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid task token") from None

    if not claims.get("email_verified") or claims.get("email") != task_service_account():
        raise HTTPException(status_code=403, detail="Not the task service account")


class StepTask(BaseModel):
    run_id: str


@router.post("/step", dependencies=[Depends(verify_task_token)])
def execute_step(body: StepTask) -> dict:
    get_runner().execute_next_step(body.run_id)
    return {"ok": True}
