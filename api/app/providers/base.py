"""Common provider interface (docs/plan/03): submit/check + fake mode.

Real implementations land with their pipeline phase (P1.2 transcribe/llm,
P2.1 music, P3.2 video/tts). Fake mode returns deterministic outputs so every
pipeline is testable without keys or spend.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum


class JobStatus(StrEnum):
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


@dataclass
class ProviderJob:
    id: str
    status: JobStatus
    output: dict | None = None
    error: str | None = None
    cost_estimate_usd: float = 0.0


class Provider(ABC):
    name: str

    @abstractmethod
    def submit(self, args: dict) -> ProviderJob: ...

    @abstractmethod
    def check(self, job_id: str) -> ProviderJob: ...


class FakeProvider(Provider):
    """Deterministic synchronous fake: submit() completes immediately."""

    def __init__(self, name: str, output_fn=None, cost: float = 0.0) -> None:
        self.name = name
        self._output_fn = output_fn or (lambda args: {"echo": args})
        self._cost = cost
        self._jobs: dict[str, ProviderJob] = {}

    def submit(self, args: dict) -> ProviderJob:
        job = ProviderJob(
            id=f"fake-{self.name}-{len(self._jobs) + 1}",
            status=JobStatus.DONE,
            output=self._output_fn(args),
            cost_estimate_usd=self._cost,
        )
        self._jobs[job.id] = job
        return job

    def check(self, job_id: str) -> ProviderJob:
        return self._jobs[job_id]
