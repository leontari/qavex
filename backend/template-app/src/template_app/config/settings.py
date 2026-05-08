# It's a place for Pydantic configs like:
# - envs
# - bd
# - redis
# - JWT
# - CORS
# - debug
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    log_level: str = "INFO"

settings = Settings()
