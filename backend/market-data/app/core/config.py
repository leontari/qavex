"""Configs."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"

settings = Settings()
