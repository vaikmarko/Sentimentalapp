"""Generic document persistence for entries/stories: Firestore or memory."""

from typing import Any, Protocol, cast


class DocStore(Protocol):
    def set(self, doc_id: str, data: dict[str, Any]) -> None: ...
    def get(self, doc_id: str) -> dict[str, Any] | None: ...
    def list_by_user(self, user_id: str, limit: int = 100) -> list[dict[str, Any]]: ...


class FirestoreDocStore:
    def __init__(self, collection: str) -> None:
        from google.cloud import firestore

        self._col = firestore.Client().collection(collection)

    def set(self, doc_id: str, data: dict[str, Any]) -> None:
        self._col.document(doc_id).set(data)

    def get(self, doc_id: str) -> dict[str, Any] | None:
        snap = cast(Any, self._col.document(doc_id).get())
        return cast(dict[str, Any], snap.to_dict()) if snap.exists else None

    def list_by_user(self, user_id: str, limit: int = 100) -> list[dict[str, Any]]:
        query = (
            self._col.where("user_id", "==", user_id)
            .order_by("created_at", direction="DESCENDING")
            .limit(limit)
        )
        return [cast(dict[str, Any], d.to_dict()) for d in query.stream()]


class MemoryDocStore:
    def __init__(self) -> None:
        self._docs: dict[str, dict[str, Any]] = {}

    def set(self, doc_id: str, data: dict[str, Any]) -> None:
        self._docs[doc_id] = data

    def get(self, doc_id: str) -> dict[str, Any] | None:
        return self._docs.get(doc_id)

    def list_by_user(self, user_id: str, limit: int = 100) -> list[dict[str, Any]]:
        mine = [d for d in self._docs.values() if d.get("user_id") == user_id]
        mine.sort(key=lambda d: d.get("created_at", ""), reverse=True)
        return mine[:limit]
