"""Provider lookup honoring the fake_providers setting."""

import json

from app.core.config import get_settings
from app.providers.base import FakeProvider, Provider

_instances: dict[str, Provider] = {}

_FAKE_STORY = {
    "title": "The Rice She Always Burned",
    "story": (
        "Every Sunday the kitchen filled with the same smell — rice, caught a "
        "minute too long at the bottom of the pot.\n\nI used to think it was "
        "carelessness. Now I think it was because she never once sat down "
        "while we ate."
    ),
    "language": "en",
    "signature": {"tone": "bittersweet", "themes": ["family", "memory"], "people": ["ema"]},
}


def _fake_llm_output(args: dict) -> dict:
    if args.get("purpose") == "crisis":
        return {"text": json.dumps({"flag": False, "reason": ""})}
    return {"text": json.dumps(_FAKE_STORY)}


def _build_fake(name: str) -> Provider:
    if name == "transcribe":
        return FakeProvider(
            "transcribe",
            lambda a: {
                "text": (
                    "Every Sunday my mother cooked rice and she always burned it a "
                    "little. I used to find it annoying and now I miss that smell."
                ),
                "language": "en",
            },
            cost=0.006,
        )
    if name == "llm":
        return FakeProvider("llm", _fake_llm_output, cost=0.02)
    if name == "music":
        return FakeProvider("music", lambda a: {"audio_url": "fake://song.mp3"}, cost=0.045)
    if name == "video":
        return FakeProvider("video", lambda a: {"video_url": "fake://film.mp4"}, cost=1.50)
    if name == "tts":
        return FakeProvider("tts", lambda a: {"audio_url": "fake://voice.mp3"}, cost=0.05)
    raise KeyError(name)


def _build_real(name: str) -> Provider:
    settings = get_settings()
    if name in ("transcribe", "llm"):
        if not settings.openai_api_key:
            raise RuntimeError(
                f"Provider '{name}' needs OPENAI_API_KEY; set it or enable FAKE_PROVIDERS."
            )
        from app.providers.openai import OpenAIChat, OpenAITranscribe

        return OpenAITranscribe() if name == "transcribe" else OpenAIChat()
    raise NotImplementedError(
        f"Real provider '{name}' lands with its pipeline phase (see docs/plan/05); "
        "set FAKE_PROVIDERS=true until then."
    )


def get_provider(name: str) -> Provider:
    mode = "fake" if get_settings().fake_providers else "real"
    key = f"{mode}:{name}"
    if key not in _instances:
        _instances[key] = _build_fake(name) if mode == "fake" else _build_real(name)
    return _instances[key]
