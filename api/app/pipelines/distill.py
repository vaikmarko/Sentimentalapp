"""The distill pipeline: entry (voice or text) -> story (docs/plan/01 step 3).

Steps:
  transcribe  voice entries only; text entries seed the transcript directly
  distill     LLM renders distill@v1 -> {title, story, language, signature}
  safety      crisis screen (crisis-detect@v1); flags, never blocks
  finalize    persists the story doc and links it to the entry
"""

import json
from datetime import UTC, datetime
from uuid import uuid4

from app.clients.media import get_media_store
from app.core.recommend import recommend_format
from app.pipelines.models import PipelineRun, PipelineStep
from app.pipelines.runner import register_pipeline
from app.prompts.loader import load_prompt
from app.providers.registry import get_provider
from app.stores import collections

PIPELINE_TYPE = "distill"

ALLOWED_TONES = {"joy", "bittersweet", "grief", "pride", "calm", "longing", "fear", "wonder"}


def _entry(run: PipelineRun) -> dict:
    seed = run.step("seed").output or {}
    entry = collections.entries().get(seed["entry_id"])
    if entry is None:
        raise RuntimeError(f"Entry {seed['entry_id']} not found")
    return entry


def _seed(run: PipelineRun) -> dict:
    return run.step("seed").output or {}


def _transcribe(run: PipelineRun) -> dict:
    entry = _entry(run)
    if entry["source"] == "text":
        return {"text": entry["transcript"], "language": entry.get("language", "")}
    audio = get_media_store().read(entry["audio_ref"])
    job = get_provider("transcribe").submit(
        {
            "audio": audio,
            "mime_type": entry["mime_type"],
            "duration_ms": entry.get("duration_ms", 120_000),
        }
    )
    run.step("transcribe").cost_estimate_usd = job.cost_estimate_usd
    return job.output or {}


def _parse_json(text: str) -> dict:
    # Models occasionally wrap JSON in code fences despite instructions.
    cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    return json.loads(cleaned)


def _distill(run: PipelineRun) -> dict:
    transcript = (run.step("transcribe").output or {})["text"]
    prompt = load_prompt("distill@v1")
    job = get_provider("llm").submit(
        {
            "prompt": prompt.render(transcript=transcript),
            "purpose": "distill",
            "temperature": float(prompt.meta.get("temperature", "0.7")),
        }
    )
    run.step("distill").cost_estimate_usd = job.cost_estimate_usd
    parsed = _parse_json((job.output or {})["text"])

    signature = parsed.get("signature", {})
    if signature.get("tone") not in ALLOWED_TONES:
        signature["tone"] = "calm"
    return {
        "title": str(parsed["title"]).strip(),
        "story": str(parsed["story"]).strip(),
        "language": parsed.get("language", ""),
        "signature": {
            "tone": signature["tone"],
            "themes": [str(t) for t in signature.get("themes", [])][:3],
            "people": [str(p) for p in signature.get("people", [])][:5],
        },
        "prompt_ref": prompt.ref,
    }


def _safety(run: PipelineRun) -> dict:
    transcript = (run.step("transcribe").output or {})["text"]
    prompt = load_prompt("crisis-detect@v1")
    job = get_provider("llm").submit(
        {"prompt": prompt.render(transcript=transcript), "purpose": "crisis", "temperature": 0.0}
    )
    run.step("safety").cost_estimate_usd = job.cost_estimate_usd
    try:
        parsed = _parse_json((job.output or {})["text"])
        return {"flag": bool(parsed.get("flag")), "reason": str(parsed.get("reason", ""))}
    except (json.JSONDecodeError, KeyError):
        return {"flag": False, "reason": ""}  # screening must never break the loop


def _finalize(run: PipelineRun) -> dict:
    entry = _entry(run)
    distilled = run.step("distill").output or {}
    safety = run.step("safety").output or {}
    story_id = uuid4().hex
    story = {
        "id": story_id,
        "user_id": run.user_id,
        "entry_id": entry["id"],
        "title": distilled["title"],
        "story": distilled["story"],
        "language": distilled["language"],
        "signature": distilled["signature"],
        "recommendation": recommend_format(distilled["signature"]),
        "support_flag": safety.get("flag", False),
        "prompt_ref": distilled.get("prompt_ref", ""),
        "created_at": datetime.now(UTC).isoformat(),
    }
    collections.stories().set(story_id, story)
    entry["story_id"] = story_id
    entry["status"] = "done"
    collections.entries().set(entry["id"], entry)
    return {"story_id": story_id}


def new_distill_run(user_id: str, entry_id: str) -> PipelineRun:
    return PipelineRun(
        type=PIPELINE_TYPE,
        user_id=user_id,
        steps=[
            PipelineStep(name="seed", output={"entry_id": entry_id}),
            PipelineStep(name="transcribe"),
            PipelineStep(name="distill"),
            PipelineStep(name="safety"),
            PipelineStep(name="finalize"),
        ],
    )


register_pipeline(
    PIPELINE_TYPE,
    {
        "seed": _seed,
        "transcribe": _transcribe,
        "distill": _distill,
        "safety": _safety,
        "finalize": _finalize,
    },
)
