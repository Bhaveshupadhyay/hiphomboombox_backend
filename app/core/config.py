from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_USER: str=''
    POSTGRES_PASSWORD: str=''
    POSTGRES_HOST: str=''
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: str | None = None

    # Upstash Redis
    UPSTASH_REDIS_REST_URL: str = ""
    UPSTASH_REDIS_REST_TOKEN: str = ""

settings = Settings()
