from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://admin:password@mongo:27017/?authSource=admin&directConnection=true"
    SECRET_KEY: str = "CHAVE_SUPER_SECRETA_PADRAO"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()