"""Firebase ID-token verification as a FastAPI dependency."""

import logging
from contextlib import suppress

import firebase_admin
from fastapi import Depends, HTTPException, Request
from firebase_admin import auth as firebase_auth
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AuthedUser(BaseModel):
    uid: str
    email: str | None = None
    name: str | None = None


def _ensure_app() -> None:
    if not firebase_admin._apps:
        # Cloud Run uses ambient credentials; local dev uses GOOGLE_APPLICATION_CREDENTIALS.
        firebase_admin.initialize_app()


async def get_current_user(request: Request) -> AuthedUser:
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = header.removeprefix("Bearer ").strip()
    try:
        _ensure_app()
        decoded = firebase_auth.verify_id_token(token)
    except Exception:
        logger.info("Token verification failed", exc_info=True)
        raise HTTPException(status_code=401, detail="Invalid token") from None
    return AuthedUser(
        uid=decoded["uid"],
        email=decoded.get("email"),
        name=decoded.get("name"),
    )


CurrentUser = Depends(get_current_user)


def delete_auth_user(uid: str) -> None:
    """Remove the Firebase Auth record so the person is signed out everywhere.

    No-op in the test environment (no Firebase project); an already-missing
    user is treated as deleted.
    """
    from app.core.config import get_settings

    if get_settings().environment == "test":
        return
    _ensure_app()
    with suppress(firebase_auth.UserNotFoundError):
        firebase_auth.delete_user(uid)
