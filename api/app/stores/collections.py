"""Named doc-store accessors (entries, stories) honoring the environment."""

from functools import lru_cache

from app.core.config import get_settings
from app.stores.docs import DocStore, FirestoreDocStore, MemoryDocStore


@lru_cache
def _store(collection: str) -> DocStore:
    if get_settings().environment == "test":
        return MemoryDocStore()
    return FirestoreDocStore(collection)


def entries() -> DocStore:
    return _store("v2_entries")


def stories() -> DocStore:
    return _store("v2_stories")


def reset_for_tests() -> None:
    _store.cache_clear()
