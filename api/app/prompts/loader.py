"""Prompt assets: versioned markdown files with front-matter (docs/plan/06)."""

from functools import lru_cache
from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets"


class PromptAsset:
    def __init__(self, name: str, version: int, meta: dict[str, str], template: str) -> None:
        self.name = name
        self.version = version
        self.meta = meta
        self.template = template

    @property
    def ref(self) -> str:
        return f"{self.name}@v{self.version}"

    def render(self, **kwargs: str) -> str:
        text = self.template
        for key, value in kwargs.items():
            text = text.replace("{" + key + "}", value)
        return text


@lru_cache
def load_prompt(ref: str) -> PromptAsset:
    """Load e.g. 'distill@v1' from assets/distill@v1.md."""
    path = ASSETS_DIR / f"{ref}.md"
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise ValueError(f"Prompt {ref} is missing front-matter")
    _, front, body = raw.split("---", 2)
    meta: dict[str, str] = {}
    for line in front.strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    name, _, version = ref.partition("@v")
    return PromptAsset(name, int(version), meta, body.strip())
