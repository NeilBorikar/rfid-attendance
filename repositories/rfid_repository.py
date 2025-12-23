from typing import Optional, Dict
from core import MongoDB
from repositories.base_repository import BaseRepository


class RFIDRepository(BaseRepository):

    def __init__(self):
        db = MongoDB.get_database()
        super().__init__(db["rfid_cards"])

    def get_active_by_uid(self, uid: str) -> Optional[Dict]:
        return self.find_one({
            "uid": uid,
            "is_active": True
        })
