"""Rule-based format recommendation v1 (recommend-format@v1 becomes an LLM
asset later; rules first per docs/plan/01 step 5). Reasons are bilingual so
the UI can match the story's language."""

_BY_TONE: dict[str, tuple[str, str, str]] = {
    "joy": (
        "song",
        "this one has a melody in it already",
        "selles on juba viis sees",
    ),
    "bittersweet": (
        "song",
        "this wants to be a song — the kind you play twice",
        "see tahab olla laul — selline, mida kuulad kaks korda",
    ),
    "grief": (
        "story",
        "some things just want to be said plainly and kept",
        "mõned asjad tahavad lihtsalt öeldud ja hoitud saada",
    ),
    "pride": (
        "film",
        "this deserves to be seen, not just read",
        "see väärib nägemist, mitte ainult lugemist",
    ),
    "calm": (
        "story",
        "a quiet page for a quiet moment",
        "vaikne lehekülg vaikse hetke jaoks",
    ),
    "longing": (
        "song",
        "longing always sings better than it speaks",
        "igatsus laulab alati paremini, kui räägib",
    ),
    "fear": (
        "story",
        "naming it on a page makes it smaller",
        "lehele kirjutatuna muutub see väiksemaks",
    ),
    "wonder": (
        "film",
        "this one needs pictures",
        "see vajab pilte",
    ),
}

_DEFAULT = ("story", "a page of your chronicle", "lehekülg sinu kroonikas")


def recommend_format(signature: dict) -> dict:
    fmt, reason_en, reason_et = _BY_TONE.get(signature.get("tone", ""), _DEFAULT)
    return {"format": fmt, "reason": {"en": reason_en, "et": reason_et}}
