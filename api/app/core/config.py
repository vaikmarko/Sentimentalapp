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

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
