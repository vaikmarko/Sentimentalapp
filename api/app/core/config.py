from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "test"  # test | production
    gcp_project: str = "sentimental-f95e6"
    region: str = "europe-west1"

    # When true, provider modules return deterministic fake outputs (tests, local dev).
    fake_providers: bool = True
    # When true, pipeline steps execute inline instead of via Cloud Tasks (tests, local dev).
    tasks_inline: bool = True
    # Cloud Tasks queue + worker base URL (used when tasks_inline is false).
    tasks_queue: str = "pipeline-steps"
    worker_base_url: str = ""

    sentry_dsn: str = ""
    openai_api_key: str = ""
    fal_key: str = ""

    # Media storage: "local" writes under upload_dir (dev/test); "gcs" uses the bucket.
    storage_mode: str = "local"
    upload_dir: str = "var/uploads"
    gcs_bucket: str = "sentimental-audio-uploads"

    # Model choices (override per environment without code changes).
    llm_model: str = "gpt-4o-mini"
    transcribe_model: str = "gpt-4o-mini-transcribe"
    openai_base_url: str = "https://api.openai.com/v1"

    # Per-user budget guardrail (docs/plan/07): max entries distilled per day.
    daily_entry_limit: int = 20

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
