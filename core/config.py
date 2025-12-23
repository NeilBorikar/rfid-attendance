import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    """
    Centralized application configuration.
    Reads all environment variables and exposes them safely.
    """

    DB_TYPE: str = os.getenv("DB_TYPE", "mongodb")
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")

    @classmethod
    def validate(cls):
        """
        Fail fast if required configuration is missing.
        """
        if cls.DB_TYPE != "mongodb":
            raise ValueError("Unsupported DB_TYPE. Only 'mongodb' is supported.")

        if not cls.MONGO_URI:
            raise ValueError("MONGO_URI is not set in .env")

        if not cls.MONGO_DB_NAME:
            raise ValueError("MONGO_DB_NAME is not set in .env")


# Validate settings at import time
Settings.validate()
