from pymongo import MongoClient
from pymongo.database import Database

from app.settings import settings   # ✅ FIXED (import instance only)


class MongoDB:
    """
    MongoDB connection manager (Singleton-style).
    """

    _client: MongoClient = None
    _database: Database = None

    @classmethod
    def connect(cls):
        """
        Establish MongoDB connection.
        """
        if cls._client is None:
            cls._client = MongoClient(
                settings.MONGO_URI,
                serverSelectionTimeoutMS=5000,
                
            )

            # Ping to ensure connection works
            cls._client.admin.command("ping")

            # ✅ FIX: use loaded settings instance
            cls._database = cls._client[settings.MONGO_DB_NAME]

        return cls._database

    @classmethod
    def get_database(cls) -> Database:
        """
        Get MongoDB database instance.
        """
        if cls._database is None:
            return cls.connect()
        return cls._database

    @classmethod
    def close(cls):
        """
        Close MongoDB connection gracefully.
        """
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._database = None
