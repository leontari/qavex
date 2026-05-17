class DatabaseSettings(BaseSettings): ...


class RedisSettings(BaseSettings): ...


class AppSettings(BaseSettings):
    database: DatabaseSettings
    redis: RedisSettings
