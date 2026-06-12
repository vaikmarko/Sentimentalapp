"""Demo pipeline endpoints proving the async machinery (F0.2). Removed in Phase 1."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.auth import AuthedUser, CurrentUser
from app.pipelines.echo import new_echo_run
from app.routes.deps import get_runner

router = APIRouter(tags=["demo"])


class EchoRequest(BaseModel):
    text: str = Field(min_length=1, max_length=500)


@router.post("/demo/echo")
def start_echo(body: EchoRequest, user: AuthedUser = CurrentUser) -> dict:
    run = get_runner().start(new_echo_run(user.uid, body.text))
    return {"run_id": run.id, "status": run.status}


@router.get("/demo/echo/{run_id}")
def get_echo(run_id: str, user: AuthedUser = CurrentUser) -> dict:
    run = get_runner().store.get(run_id)
    if run is None or run.user_id != user.uid:
        raise HTTPException(status_code=404, detail="Run not found")
    return {
        "run_id": run.id,
        "status": run.status,
        "steps": [{"name": s.name, "status": s.status} for s in run.steps],
        "result": run.step("shout").output,
        "cost_usd": run.total_cost_usd(),
    }
