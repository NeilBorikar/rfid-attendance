from datetime import datetime
from core import MongoDB
from repositories.base_repository import BaseRepository


class AttendanceRepository(BaseRepository):

    def __init__(self):
        db = MongoDB.get_database()
        super().__init__(db["attendance_events"])

    def create_event(self, event: dict):
        event["created_at"] = datetime.utcnow()
        return self.insert_one(event)

    def event_exists(self, uid: str, event_type: str, event_time: datetime) -> bool:
        return self.exists({
            "uid": uid,
            "event_type": event_type,
            "event_time": event_time
        })
