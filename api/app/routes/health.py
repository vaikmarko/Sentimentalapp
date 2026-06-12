import os

from fastapi import APIRouter

router = APIRouter(tags=["meta"])


@router.get("/healthz")
def healthz() -> dict:
    return {"ok": True}


@router.get("/version")
def version() -> dict:
    return {
        "version": os.getenv("APP_VERSION", "dev"),
        "revision": os.getenv("K_REVISION", "local"),
    }
