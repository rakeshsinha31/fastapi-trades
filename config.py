from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "Trade APIs"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb+srv://admin:admin@cluster0.e1lvn.mongodb.net"
    DB_NAME: str = "fastapi"


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
