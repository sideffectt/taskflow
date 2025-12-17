from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongo_uri: str = 'mongodb://localhost:27017'
    database_name: str = 'taskflow'
    app_name: str = 'TaskFlow API'
    app_version: str = '1.0.0'
    debug: bool = False
    
    model_config = SettingsConfigDict(
        env_file = '.env',
        env_file_encoding = 'utf-8'
    )   
    
settings = Settings()