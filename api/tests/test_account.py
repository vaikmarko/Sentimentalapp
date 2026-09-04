import io
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.auth import AuthedUser, get_current_user
from app.main import app
from app.routes import deps
from app.stores import collections


@pytest.fixture(autouse=True)
def fresh_stores():
    collections.reset_for_tests()
    yield
    collections.reset_for_tests()


def test_delete_me_erases_everything_including_audio(client, tmp_path, monkeypatch):
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path))
    from app.core.config import get_settings

    get_settings.cache_clear()

    client.post("/api/entries/text", json={"text": "A long enough text about my quiet morning."})
    audio = io.BytesIO(b"\x1aE\xdf\xa3 fake webm bytes for the fake provider")
    res = client.post(
        "/api/entries/audio",
        files={"file": ("entry.webm", audio, "audio/webm")},
        data={"duration_ms": "5000"},
    )
    entry_id = res.json()["entry_id"]
    assert len(list(Path(tmp_path).iterdir())) == 1  # the recording is on disk
    run_id = collections.entries().get(entry_id)["run_id"]

    deleted = client.delete("/api/me")
    assert deleted.status_code == 200
    assert deleted.json()["deleted"] == {
        "recordings": 1,
        "entries": 2,
        "stories": 2,
        "runs": 2,
    }

    assert client.get("/api/stories").json()["stories"] == []
    assert client.get(f"/api/entries/{entry_id}").status_code == 404
    assert deps.get_runner().store.get(run_id) is None
    assert list(Path(tmp_path).iterdir()) == []  # recording gone too

    get_settings.cache_clear()


def test_delete_me_only_touches_the_caller(client):
    client.post("/api/entries/text", json={"text": "A long enough text about my quiet morning."})

    app.dependency_overrides[get_current_user] = lambda: AuthedUser(uid="someone-else")
    client.post("/api/entries/text", json={"text": "Another person's evening, also long enough."})
    assert client.delete("/api/me").json()["deleted"]["stories"] == 1

    app.dependency_overrides[get_current_user] = lambda: AuthedUser(uid="test-uid")
    assert len(client.get("/api/stories").json()["stories"]) == 1


def test_api_requires_auth():
    # No dependency override here — the real auth dependency must reject.
    with TestClient(app) as raw:
        assert raw.get("/api/stories").status_code == 401
        assert raw.delete("/api/me").status_code == 401
        assert raw.post("/api/entries/text", json={"text": "x" * 30}).status_code == 401


def test_worker_route_is_not_mounted_in_inline_mode(client):
    # TASKS_INLINE=true (default) -> nothing enqueues, so nothing should listen.
    assert client.post("/internal/tasks/step", json={"run_id": "x"}).status_code == 404
