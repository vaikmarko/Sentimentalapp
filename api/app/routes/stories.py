"""Stories: the Chronicle's read surface + the daily question."""

import json
import random
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core.auth import AuthedUser, CurrentUser
from app.stores import collections

router = APIRouter(tags=["stories"])

_QUESTIONS = json.loads(
    (Path(__file__).parent.parent / "assets" / "daily_questions.json").read_text(encoding="utf-8")
)["universal"]


@router.get("/stories")
def list_stories(user: AuthedUser = CurrentUser) -> dict:
    stories = collections.stories().list_by_user(user.uid)
    return {"stories": stories}


@router.get("/stories/{story_id}")
def get_story(story_id: str, user: AuthedUser = CurrentUser) -> dict:
    story = collections.stories().get(story_id)
    if story is None or story["user_id"] != user.uid:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.get("/daily-question")
def daily_question(user: AuthedUser = CurrentUser) -> dict:
    """Deterministic per user per day; context-aware selection lands in P1.4+."""
    day = datetime.now(UTC).date().toordinal()
    rng = random.Random(f"{user.uid}:{day}")
    question = rng.choice(_QUESTIONS)
    return {"id": question["id"], "en": question["en"], "et": question["et"]}
