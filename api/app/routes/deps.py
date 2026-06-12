"""Shared singletons. Kept tiny on purpose; revisit if wiring grows."""

from functools import lru_cache

from app.core.config import get_settings
from app.pipelines.runner import PipelineRunner
from app.pipelines.store import FirestoreRunStore, MemoryRunStore


class RunnerHolder(PipelineRunner):
    """PipelineRunner with its store exposed for route handlers."""

    def __init__(self) -> None:
        settings = get_settings()
        if settings.tasks_inline:
            store = MemoryRunStore() if settings.environment == "test" else FirestoreRunStore()
            super().__init__(store, enqueue=None)
        else:
            from app.clients.tasks import enqueue_step

            store = FirestoreRunStore()
            super().__init__(store, enqueue=enqueue_step)
        self.store = store


@lru_cache
def get_runner() -> RunnerHolder:
    return RunnerHolder()
