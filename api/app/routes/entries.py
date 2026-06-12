"""Entries: the capture side of the core loop."""

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.clients.media import get_media_store
from app.core.auth import AuthedUser, CurrentUser
from app.core.config import get_settings
from app.pipelines.distill import new_distill_run
from app.routes.deps import get_runner
from app.stores import collections

router = APIRouter(tags=["entries"])

ALLOWED_MIME = {"audio/webm", "audio/mp4", "audio/mpeg", "audio/ogg"}
MAX_AUDIO_BYTES = 25 * 1024 * 1024  # ~25MB covers >10 min of opus comfortably


def _check_daily_budget(user_id: str) -> None:
    today = datetime.now(UTC).date().isoformat()
    recent = collections.entries().list_by_user(user_id, limit=get_settings().daily_entry_limit)
    todays = [e for e in recent if str(e.get("created_at", "")).startswith(today)]
    if len(todays) >= get_settings().daily_entry_limit:
        raise HTTPException(
            status_code=429,
            detail="The studio closes for the night after this many stories — see you tomorrow.",
        )


def _create_entry(user: AuthedUser, **fields) -> dict:
    entry = {
        "id": uuid4().hex,
        "user_id": user.uid,
        "status": "distilling",
        "story_id": None,
        "created_at": datetime.now(UTC).isoformat(),
        **fields,
    }
    collections.entries().set(entry["id"], entry)
    run = get_runner().start(new_distill_run(user.uid, entry["id"]))
    entry["run_id"] = run.id
    collections.entries().set(entry["id"], entry)
    return entry


@router.post("/entries/audio")
async def create_audio_entry(
    file: UploadFile = File(...),
    duration_ms: int = Form(0),
    user: AuthedUser = CurrentUser,
) -> dict:
    _check_daily_budget(user.uid)
    mime = (file.content_type or "").split(";")[0].strip()
    if mime not in ALLOWED_MIME:
        raise HTTPException(status_code=415, detail=f"Unsupported audio type: {mime}")
    data = await file.read()
    if len(data) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Recording too large")
    if not data:
        raise HTTPException(status_code=400, detail="Empty recording")

    suffix = ".mp4" if "mp4" in mime else ".webm"
    ref = get_media_store().save(data, suffix)
    entry = _create_entry(
        user, source="voice", audio_ref=ref, mime_type=mime, duration_ms=duration_ms
    )
    return {"entry_id": entry["id"], "status": entry["status"]}


class TextEntry(BaseModel):
    text: str = Field(min_length=20, max_length=20_000)


@router.post("/entries/text")
def create_text_entry(body: TextEntry, user: AuthedUser = CurrentUser) -> dict:
    _check_daily_budget(user.uid)
    entry = _create_entry(user, source="text", transcript=body.text)
    return {"entry_id": entry["id"], "status": entry["status"]}


@router.get("/entries/{entry_id}")
def get_entry(entry_id: str, user: AuthedUser = CurrentUser) -> dict:
    entry = collections.entries().get(entry_id)
    if entry is None or entry["user_id"] != user.uid:
        raise HTTPException(status_code=404, detail="Entry not found")

    run = get_runner().store.get(entry.get("run_id", ""))
    status = entry["status"]
    if run is not None and run.status == "failed" and status != "done":
        status = "failed"

    story = None
    if entry.get("story_id"):
        story = collections.stories().get(entry["story_id"])
    return {"entry_id": entry_id, "status": status, "story": story}
