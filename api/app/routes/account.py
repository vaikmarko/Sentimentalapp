"""Account: the GDPR erasure path. One call removes everything a person left here."""

import logging

from fastapi import APIRouter

from app.clients.media import get_media_store
from app.core.auth import AuthedUser, CurrentUser, delete_auth_user
from app.routes.deps import get_runner
from app.stores import collections

logger = logging.getLogger(__name__)

router = APIRouter(tags=["account"])

# Firestore queries are paged; loop until a user's collection is empty.
_PAGE = 500


def erase_user(uid: str) -> dict[str, int]:
    """Delete recordings, entries, stories, pipeline runs and the sign-in record."""
    counts = {"recordings": 0, "entries": 0, "stories": 0, "runs": 0}
    media = get_media_store()

    while entries := collections.entries().list_by_user(uid, limit=_PAGE):
        for entry in entries:
            if ref := entry.get("audio_ref"):
                try:
                    media.delete(ref)
                    counts["recordings"] += 1
                except Exception:
                    # A stranded blob must not block the person's right to erasure;
                    # it is logged so it can be swept by hand.
                    logger.exception("Could not delete recording %s", ref)
            collections.entries().delete(entry["id"])
            counts["entries"] += 1

    while stories := collections.stories().list_by_user(uid, limit=_PAGE):
        for story in stories:
            collections.stories().delete(story["id"])
            counts["stories"] += 1

    store = get_runner().store
    for run_id in store.list_ids_by_user(uid):
        store.delete(run_id)
        counts["runs"] += 1

    delete_auth_user(uid)
    logger.info("Erased user %s: %s", uid, counts)
    return counts


@router.delete("/me")
def delete_me(user: AuthedUser = CurrentUser) -> dict:
    return {"deleted": erase_user(user.uid)}
