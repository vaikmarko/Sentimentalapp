"""Media blob storage: local disk for dev/test, GCS for deployment."""

from pathlib import Path
from typing import Protocol
from uuid import uuid4

from app.core.config import get_settings


class MediaStore(Protocol):
    def save(self, data: bytes, suffix: str) -> str:
        """Persist bytes, return an opaque storage ref."""
        ...

    def read(self, ref: str) -> bytes: ...

    def delete(self, ref: str) -> None:
        """Remove the blob; a ref that is already gone is not an error."""
        ...


class LocalMediaStore:
    def __init__(self, root: str | None = None) -> None:
        self._root = Path(root or get_settings().upload_dir)
        self._root.mkdir(parents=True, exist_ok=True)

    def save(self, data: bytes, suffix: str) -> str:
        name = f"{uuid4().hex}{suffix}"
        (self._root / name).write_bytes(data)
        return f"local://{name}"

    def read(self, ref: str) -> bytes:
        return (self._root / ref.removeprefix("local://")).read_bytes()

    def delete(self, ref: str) -> None:
        (self._root / ref.removeprefix("local://")).unlink(missing_ok=True)


class GcsMediaStore:
    def __init__(self) -> None:
        from google.cloud import storage  # type: ignore[attr-defined]

        self._bucket = storage.Client().bucket(get_settings().gcs_bucket)

    def save(self, data: bytes, suffix: str) -> str:
        name = f"v2/entries/{uuid4().hex}{suffix}"
        self._bucket.blob(name).upload_from_string(data)
        return f"gs://{get_settings().gcs_bucket}/{name}"

    def read(self, ref: str) -> bytes:
        name = ref.removeprefix(f"gs://{get_settings().gcs_bucket}/")
        return self._bucket.blob(name).download_as_bytes()

    def delete(self, ref: str) -> None:
        from contextlib import suppress

        from google.api_core.exceptions import NotFound

        name = ref.removeprefix(f"gs://{get_settings().gcs_bucket}/")
        with suppress(NotFound):
            self._bucket.blob(name).delete()


def get_media_store() -> MediaStore:
    if get_settings().storage_mode == "gcs":
        return GcsMediaStore()
    return LocalMediaStore()
