"""Pipeline execution: advances runs step by step.

In deployment each step executes as a Cloud Task hitting /internal/tasks/step,
so steps survive instance restarts and retry independently. With tasks_inline
(local dev, tests) steps execute synchronously in-process.
"""

import logging
from collections.abc import Callable
from datetime import UTC, datetime

from app.core.config import get_settings
from app.pipelines.models import PipelineRun, RunStatus, StepStatus
from app.pipelines.store import RunStore

logger = logging.getLogger(__name__)

# Registry: pipeline type -> step name -> handler(run, step_output_context) -> output dict
StepHandler = Callable[[PipelineRun], dict]
_REGISTRY: dict[str, dict[str, StepHandler]] = {}


def register_pipeline(pipeline_type: str, steps: dict[str, StepHandler]) -> None:
    _REGISTRY[pipeline_type] = steps


def step_names(pipeline_type: str) -> list[str]:
    return list(_REGISTRY[pipeline_type].keys())


class PipelineRunner:
    def __init__(self, store: RunStore, enqueue: Callable[[str], None] | None = None) -> None:
        """enqueue schedules execute_next_step(run_id) via Cloud Tasks; None = inline."""
        self._store = store
        self._enqueue = enqueue

    def start(self, run: PipelineRun) -> PipelineRun:
        self._store.save(run)
        self._advance(run.id)
        return self._store.get(run.id) or run

    def execute_next_step(self, run_id: str) -> None:
        """Worker entrypoint: run exactly one pending step, then schedule the next."""
        run = self._store.get(run_id)
        if run is None:
            logger.warning("Pipeline run %s not found", run_id)
            return
        step = run.next_pending_step()
        if step is None:
            run.status = RunStatus.DONE
            run.updated_at = datetime.now(UTC)
            self._store.save(run)
            return

        handler = _REGISTRY[run.type][step.name]
        step.status = StepStatus.RUNNING
        step.started_at = datetime.now(UTC)
        self._store.save(run)
        try:
            step.output = handler(run)
            step.status = StepStatus.DONE
        except Exception as exc:
            logger.exception("Step %s of run %s failed", step.name, run_id)
            step.status = StepStatus.FAILED
            step.error = str(exc)
            run.status = RunStatus.FAILED
        finally:
            step.finished_at = datetime.now(UTC)
            run.updated_at = datetime.now(UTC)
            self._store.save(run)

        if step.status == StepStatus.DONE:
            self._advance(run_id)

    def retry_failed_step(self, run_id: str) -> None:
        """Reset the failed step to pending and resume — idempotent recovery."""
        run = self._store.get(run_id)
        if run is None:
            return
        for step in run.steps:
            if step.status == StepStatus.FAILED:
                step.status = StepStatus.PENDING
                step.error = None
        run.status = RunStatus.RUNNING
        self._store.save(run)
        self._advance(run_id)

    def _advance(self, run_id: str) -> None:
        if self._enqueue is not None and not get_settings().tasks_inline:
            self._enqueue(run_id)
        else:
            self.execute_next_step(run_id)
