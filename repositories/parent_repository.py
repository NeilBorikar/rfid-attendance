from typing import List, Dict
from core import MongoDB
from repositories.base_repository import BaseRepository


class ParentRepository(BaseRepository):

    def __init__(self):
        db = MongoDB.get_database()
        super().__init__(db["parents"])

    def get_by_student_id(self, student_id: str) -> List[Dict]:
        return self.find_many({"student_id": student_id})

    def get_whatsapp_enabled(self, student_id: str) -> List[Dict]:
        return self.find_many({
            "student_id": student_id,
            "whatsapp_enabled": True
        })
