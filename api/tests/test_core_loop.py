import io

import pytest

from app.stores import collections


@pytest.fixture(autouse=True)
def fresh_stores():
    collections.reset_for_tests()
    yield
    collections.reset_for_tests()


def test_text_entry_distills_into_story(client):
    res = client.post(
        "/api/entries/text",
        json={"text": "Every Sunday my mother cooked rice and she always burned it a little."},
    )
    assert res.status_code == 200
    entry_id = res.json()["entry_id"]

    result = client.get(f"/api/entries/{entry_id}").json()
    assert result["status"] == "done"
    story = result["story"]
    assert story["title"] == "The Rice She Always Burned"
    assert story["signature"]["tone"] == "bittersweet"
    assert story["recommendation"]["format"] == "song"
    assert story["support_flag"] is False
    assert story["prompt_ref"] == "distill@v1"


def test_audio_entry_distills_into_story(client, tmp_path, monkeypatch):
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path))
    from app.core.config import get_settings

    get_settings.cache_clear()

    fake_audio = io.BytesIO(b"\x1aE\xdf\xa3 not really webm but enough for the fake provider")
    res = client.post(
        "/api/entries/audio",
        files={"file": ("entry.webm", fake_audio, "audio/webm")},
        data={"duration_ms": "94000"},
    )
    assert res.status_code == 200, res.text
    entry_id = res.json()["entry_id"]

    result = client.get(f"/api/entries/{entry_id}").json()
    assert result["status"] == "done"
    assert result["story"]["title"] == "The Rice She Always Burned"

    get_settings.cache_clear()


def test_audio_entry_rejects_unknown_mime(client):
    res = client.post(
        "/api/entries/audio",
        files={"file": ("entry.exe", io.BytesIO(b"xx"), "application/octet-stream")},
    )
    assert res.status_code == 415


def test_story_listing_and_isolation(client):
    client.post("/api/entries/text", json={"text": "A long enough text about my quiet morning."})
    stories = client.get("/api/stories").json()["stories"]
    assert len(stories) == 1

    story_id = stories[0]["id"]
    from app.core.auth import AuthedUser, get_current_user
    from app.main import app

    app.dependency_overrides[get_current_user] = lambda: AuthedUser(uid="intruder")
    assert client.get(f"/api/stories/{story_id}").status_code == 404
    assert client.get("/api/stories").json()["stories"] == []


def test_daily_question_is_stable_within_a_day(client):
    first = client.get("/api/daily-question").json()
    second = client.get("/api/daily-question").json()
    assert first == second
    assert {"id", "en", "et"} <= first.keys()


def test_distill_prompt_renders_transcript_verbatim():
    from app.prompts.loader import load_prompt

    prompt = load_prompt("distill@v1")
    rendered = prompt.render(transcript="she always burned the rice")
    assert "she always burned the rice" in rendered
    assert "{transcript}" not in rendered
    assert "Never invent biographical facts" in rendered
    assert prompt.meta["name"] == "distill"
