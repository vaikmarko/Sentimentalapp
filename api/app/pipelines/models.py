"""The pipeline-run primitive: every artifact is produced by a tracked run.

See docs/plan/03 "The media pipeline". Rules: every step idempotent and
resumable; per-step status, provider job ids, outputs and cost estimates are
persisted so a retry re-runs only the failed step.
"""

from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field


class StepStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    WAITING_PROVIDER = "waiting_provider"  # async provider job in flight
    WAITING_HUMAN = "waiting_human"  # concierge steps (e.g. Studio queue, doc 07)
    DONE = "done"
    FAILED = "failed"


class RunStatus(StrEnum):
    RUNNING = "running"
    WAITING = "waiting"
    DONE = "done"
    FAILED = "failed"


class PipelineStep(BaseModel):
    name: str
    status: StepStatus = StepStatus.PENDING
    provider_job_id: str | None = None
    output: dict | None = None
    error: str | None = None
    cost_estimate_usd: float = 0.0
    started_at: datetime | None = None
    finished_at: datetime | None = None


class PipelineRun(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    type: str
    user_id: str
    status: RunStatus = RunStatus.RUNNING
    steps: list[PipelineStep]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def step(self, name: str) -> PipelineStep:
        for s in self.steps:
            if s.name == name:
                return s
        raise KeyError(f"Unknown step: {name}")

    def next_pending_step(self) -> PipelineStep | None:
        return next((s for s in self.steps if s.status == StepStatus.PENDING), None)

    def total_cost_usd(self) -> float:
        return round(sum(s.cost_estimate_usd for s in self.steps), 6)
