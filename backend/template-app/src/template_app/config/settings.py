# It's a place for Pydantic configs like:
# - envs
# - bd
# - redis
# - JWT
# - CORS
# - debug
from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    log_level: str = "INFO"


settings = Settings()
