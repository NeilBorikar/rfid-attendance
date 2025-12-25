from pydantic import BaseSettings


class AppSettings(BaseSettings):
    APP_NAME: str = "RFID Attendance Backend"
    APP_ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = AppSettings()
