from datetime import datetime
from core import MongoDB
from repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository):

    def __init__(self):
        db = MongoDB.get_database()
        super().__init__(db["notification_logs"])

    def log_notification(self, payload: dict):
        payload["sent_at"] = datetime.utcnow()
        return self.insert_one(payload)
