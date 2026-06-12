"""Rule-based format recommendation v1 (recommend-format@v1 becomes an LLM
asset later; rules first per docs/plan/01 step 5)."""

_BY_TONE: dict[str, tuple[str, str]] = {
    "joy": ("song", "this one has a melody in it already"),
    "bittersweet": ("song", "this wants to be a song — the kind you play twice"),
    "grief": ("story", "some things just want to be said plainly and kept"),
    "pride": ("film", "this deserves to be seen, not just read"),
    "calm": ("story", "a quiet page for a quiet moment"),
    "longing": ("song", "longing always sings better than it speaks"),
    "fear": ("story", "naming it on a page makes it smaller"),
    "wonder": ("film", "this one needs pictures"),
}


def recommend_format(signature: dict) -> dict:
    fmt, reason = _BY_TONE.get(signature.get("tone", ""), ("story", "a page of your chronicle"))
    return {"format": fmt, "reason": reason}
