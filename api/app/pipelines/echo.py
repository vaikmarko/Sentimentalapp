"""Demo pipeline proving the run/step/task machinery end to end (F0.2)."""

from app.pipelines.models import PipelineRun, PipelineStep
from app.pipelines.runner import register_pipeline

PIPELINE_TYPE = "echo"


def _shout(run: PipelineRun) -> dict:
    message = run.step("receive").output or {}
    return {"text": str(message.get("text", "")).upper()}


def _receive(run: PipelineRun) -> dict:
    # Output was seeded at creation time; pass it through.
    return run.step("receive").output or {}


def new_echo_run(user_id: str, text: str) -> PipelineRun:
    receive = PipelineStep(name="receive", output={"text": text})
    shout = PipelineStep(name="shout")
    return PipelineRun(type=PIPELINE_TYPE, user_id=user_id, steps=[receive, shout])


register_pipeline(PIPELINE_TYPE, {"receive": _receive, "shout": _shout})
