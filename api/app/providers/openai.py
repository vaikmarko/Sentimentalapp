"""Real OpenAI providers: transcription + chat completion (sync, called from workers)."""

from uuid import uuid4

import httpx

from app.core.config import get_settings
from app.providers.base import JobStatus, Provider, ProviderJob

_TIMEOUT = httpx.Timeout(120.0, connect=10.0)


def _headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {get_settings().openai_api_key}"}


class OpenAITranscribe(Provider):
    """args: {audio: bytes, mime_type: str} -> {text, language}"""

    name = "transcribe"

    def submit(self, args: dict) -> ProviderJob:
        settings = get_settings()
        suffix = "mp4" if "mp4" in args["mime_type"] else "webm"
        response = httpx.post(
            f"{settings.openai_base_url}/audio/transcriptions",
            headers=_headers(),
            files={"file": (f"entry.{suffix}", args["audio"], args["mime_type"])},
            data={"model": settings.transcribe_model, "response_format": "json"},
            timeout=_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        minutes = float(args.get("duration_ms", 120_000)) / 60_000
        return ProviderJob(
            id=uuid4().hex,
            status=JobStatus.DONE,
            output={"text": payload["text"], "language": payload.get("language", "")},
            cost_estimate_usd=round(0.003 * minutes, 6),
        )

    def check(self, job_id: str) -> ProviderJob:
        raise NotImplementedError("Transcription completes synchronously")


class OpenAIChat(Provider):
    """args: {prompt: str, purpose: str, temperature?: float} -> {text}"""

    name = "llm"

    def submit(self, args: dict) -> ProviderJob:
        settings = get_settings()
        response = httpx.post(
            f"{settings.openai_base_url}/chat/completions",
            headers=_headers(),
            json={
                "model": settings.llm_model,
                "messages": [{"role": "user", "content": args["prompt"]}],
                "temperature": args.get("temperature", 0.7),
                "response_format": {"type": "json_object"},
            },
            timeout=_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        usage = payload.get("usage", {})
        # Rough blended estimate; exact rates tracked in the cost dashboard later.
        in_tok = usage.get("prompt_tokens", 0)
        out_tok = usage.get("completion_tokens", 0)
        cost = (in_tok * 0.15 + out_tok * 0.6) / 1e6
        return ProviderJob(
            id=payload.get("id", uuid4().hex),
            status=JobStatus.DONE,
            output={"text": payload["choices"][0]["message"]["content"]},
            cost_estimate_usd=round(cost, 6),
        )

    def check(self, job_id: str) -> ProviderJob:
        raise NotImplementedError("Chat completes synchronously")
