from typing import Optional, Dict
from core import MongoDB
from repositories.base_repository import BaseRepository


class StudentRepository(BaseRepository):

    def __init__(self):
        db = MongoDB.get_database()
        super().__init__(db["students"])

    def get_by_student_id(self, student_id: str) -> Optional[Dict]:
        return self.find_one({"student_id": student_id, "is_active": True})

    def get_by_id(self, _id) -> Optional[Dict]:
        return self.find_one({"_id": _id, "is_active": True})
