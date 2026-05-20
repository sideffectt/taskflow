from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    mongo_uri: str = "mongodb://localhost:27017"
    database_name: str = "taskflow"
    app_name: str = "TaskFlow API"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str = "change-this-in-production"
    access_token_expire_minutes: int = 1440


settings = Settings()