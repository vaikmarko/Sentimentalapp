from app.pipelines.echo import new_echo_run
from app.pipelines.models import RunStatus, StepStatus
from app.pipelines.runner import PipelineRunner, register_pipeline
from app.pipelines.store import MemoryRunStore


def test_echo_pipeline_completes_inline():
    store = MemoryRunStore()
    runner = PipelineRunner(store)
    run = runner.start(new_echo_run("u1", "hello studio"))

    final = store.get(run.id)
    assert final is not None
    assert final.status == RunStatus.DONE
    assert all(s.status == StepStatus.DONE for s in final.steps)
    assert final.step("shout").output == {"text": "HELLO STUDIO"}


def test_failed_step_is_recorded_and_retryable():
    store = MemoryRunStore()
    runner = PipelineRunner(store)

    attempts = {"n": 0}

    def flaky(run):
        attempts["n"] += 1
        if attempts["n"] == 1:
            raise RuntimeError("provider hiccup")
        return {"ok": True}

    register_pipeline("flaky", {"only": flaky})
    from app.pipelines.models import PipelineRun, PipelineStep

    run = runner.start(PipelineRun(type="flaky", user_id="u1", steps=[PipelineStep(name="only")]))

    failed = store.get(run.id)
    assert failed is not None
    assert failed.status == RunStatus.FAILED
    assert failed.step("only").error == "provider hiccup"

    runner.retry_failed_step(run.id)
    recovered = store.get(run.id)
    assert recovered is not None
    assert recovered.status == RunStatus.DONE
    assert recovered.step("only").output == {"ok": True}
