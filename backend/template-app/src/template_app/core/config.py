from pydantic_settings import BaseSettings


class Config(BaseSettings):
    env: str = "dev"
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    log_level: str = "info"

    class Config:
        env_file = ".env"
        env_prefix = "APP_"


config = Config()
