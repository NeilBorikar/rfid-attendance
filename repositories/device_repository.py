from typing import Optional, Dict
from datetime import datetime

from core import MongoDB
from repositories.base_repository import BaseRepository


class DeviceRepository(BaseRepository):

    def __init__(self):
        db = MongoDB.get_database()
        super().__init__(db["devices"])

    # =========================
    # EXISTING FUNCTIONALITY
    # =========================

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

    # =========================
    # NEW: DEVICE CONFIG SUPPORT
    # =========================

    def get_device_config(self, device_id: str) -> Optional[Dict]:
        """
        Fetch full device configuration for ESP.
        """
        return self.find_one({
            "device_id": device_id
        })

    def update_device_config(self, device_id: str, data: Dict):
        """
        Update device configuration from admin/app.
        """
        data["updated_at"] = datetime.utcnow()

        self.update_one(
            {"device_id": device_id},
            data
        )

    def get_device_by_id(self, device_id: str) -> Optional[Dict]:
        """
        Fetch device without active-status filter.
        """
        return self.find_one({
            "device_id": device_id
        })
