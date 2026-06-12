"""Persistence for pipeline runs: Firestore in deployment, memory in tests."""

from typing import Protocol, cast

from google.cloud import firestore  # provided by firebase-admin's dependency tree

from app.pipelines.models import PipelineRun

COLLECTION = "v2_pipeline_runs"


class RunStore(Protocol):
    def save(self, run: PipelineRun) -> None: ...
    def get(self, run_id: str) -> PipelineRun | None: ...


class FirestoreRunStore:
    def __init__(self, client: firestore.Client | None = None) -> None:
        self._client = client or firestore.Client()

    def save(self, run: PipelineRun) -> None:
        self._client.collection(COLLECTION).document(run.id).set(
            run.model_dump(mode="json")
        )

    def get(self, run_id: str) -> PipelineRun | None:
        snap = cast(
            firestore.DocumentSnapshot,
            self._client.collection(COLLECTION).document(run_id).get(),
        )
        if not snap.exists:
            return None
        return PipelineRun.model_validate(snap.to_dict())


class MemoryRunStore:
    def __init__(self) -> None:
        self._runs: dict[str, dict] = {}

    def save(self, run: PipelineRun) -> None:
        self._runs[run.id] = run.model_dump(mode="json")

    def get(self, run_id: str) -> PipelineRun | None:
        data = self._runs.get(run_id)
        return PipelineRun.model_validate(data) if data else None
