import json
from typing import Any, Literal

from pydantic import HttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    if isinstance(v, list):
        return v
    if isinstance(v, str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "Fraud Detection API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: list[str] | str = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        raw = self.BACKEND_CORS_ORIGINS
        if isinstance(raw, list):
            return [str(x).strip() for x in raw if str(x).strip()]
        s = raw.strip()
        if not s:
            return []
        # JSON array format from .env e.g. ["http://localhost:5173"]
        if s.startswith("["):
            try:
                parsed = json.loads(s)
                return [str(x).strip() for x in parsed if str(x).strip()]
            except json.JSONDecodeError:
                pass
        return [x.strip() for x in s.split(",") if x.strip()]

    SENTRY_DSN: HttpUrl | None = None

    # ML model path (relative to backend app root or absolute)
    MODEL_PATH: str = "app/model/model.joblib"


settings = Settings()  # type: ignore
