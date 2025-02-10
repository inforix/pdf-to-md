from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CACHE_EXPIRATION: int = 3600  # 1 hour

    class Config:
        env_file = ".env"

settings = Settings() 