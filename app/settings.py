from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_NAME: str = "RFID Attendance Backend"
    DEBUG: bool = False

    # MongoDB
    MONGO_URI: str
    MONGO_DB_NAME: str

    # Twilio
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_WHATSAPP_FROM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # VERY IMPORTANT for Railway
    )


settings = Settings()
