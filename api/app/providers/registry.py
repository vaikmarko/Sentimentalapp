"""Provider lookup honoring the fake_providers setting."""

from app.core.config import get_settings
from app.providers.base import FakeProvider, Provider

_fakes: dict[str, Provider] = {}


def _fake(name: str, output_fn, cost: float) -> Provider:
    if name not in _fakes:
        _fakes[name] = FakeProvider(name, output_fn, cost)
    return _fakes[name]


def get_provider(name: str) -> Provider:
    settings = get_settings()
    if settings.fake_providers:
        return {
            "transcribe": lambda: _fake(
                "transcribe", lambda a: {"text": "(fake transcript)", "language": "et"}, 0.006
            ),
            "llm": lambda: _fake(
                "llm", lambda a: {"text": "(fake completion)"}, 0.02
            ),
            "music": lambda: _fake(
                "music", lambda a: {"audio_url": "fake://song.mp3"}, 0.045
            ),
            "video": lambda: _fake(
                "video", lambda a: {"video_url": "fake://film.mp4"}, 1.50
            ),
            "tts": lambda: _fake(
                "tts", lambda a: {"audio_url": "fake://voice.mp3"}, 0.05
            ),
        }[name]()
    raise NotImplementedError(
        f"Real provider '{name}' lands with its pipeline phase (see docs/plan/05); "
        "set FAKE_PROVIDERS=true until then."
    )
