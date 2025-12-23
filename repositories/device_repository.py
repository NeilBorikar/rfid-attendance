from typing import Optional, Dict
from datetime import datetime
from core import MongoDB
from repositories.base_repository import BaseRepository


class DeviceRepository(BaseRepository):

    def __init__(self):
        db = MongoDB.get_database()
        super().__init__(db["devices"])

    def get_active_device(self, device_id: str) -> Optional[Dict]:
        return self.find_one({
            "device_id": device_id,
            "is_active": True
        })

    def update_last_seen(self, device_id: str):
        self.update_one(
            {"device_id": device_id},
            {"last_seen_at": datetime.utcnow()}
        )
