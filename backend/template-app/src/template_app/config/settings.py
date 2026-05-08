# It's a place for Pydantic configs like:
# - envs
# - bd
# - redis
# - JWT
# - CORS
# - debug
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    database_url: str
    redis_url: str

settings = Settings()
