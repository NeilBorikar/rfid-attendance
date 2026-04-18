from repositories import (
    StudentRepository,
    ParentRepository,
    RFIDRepository
)

from schemas.student_schema import StudentOut, StudentCreate
from utils.id_utils import normalize_uid


class StudentService:

    def __init__(self):
        self.student_repo = StudentRepository()
        self.parent_repo = ParentRepository()
        self.rfid_repo = RFIDRepository()

    def register_student(self, student_data: StudentCreate) -> StudentOut:
        """
        Register a new student in the system.
        """
        # Check if student already exists
        if self.student_repo.get_by_student_id(student_data.student_id):
            raise ValueError(f"Student with ID {student_data.student_id} already exists")

        # Create student document
        student_dict = student_data.model_dump()
        self.student_repo.insert_one(student_dict)

        return StudentOut(**student_dict)

    def resolve_student_by_uid(self, uid: str):
        """
        Resolve a student using an RFID UID.
        """

        # 1️⃣ Normalize UID for consistency
        normalized_uid = normalize_uid(uid)

        # 2️⃣ Fetch active RFID card
        rfid_card = self.rfid_repo.get_active_by_uid(normalized_uid)
        if not rfid_card:
            return None

        # 3️⃣ Fetch student record
        student = self.student_repo.get_by_student_id(
            rfid_card["student_id"]
        )

        if not student:
            return None

        # 4️⃣ Return schema-backed student (clean contract)
        return StudentOut(**student)

    def get_whatsapp_enabled_parents(self, student_id: str):
        """
        Fetch parents who have WhatsApp notifications enabled.
        """
        return self.parent_repo.get_whatsapp_enabled(student_id)

    def get_all_students(self) -> list[StudentOut]:
        students = self.student_repo.find_many({})
        return [StudentOut(**student) for student in students]

    def delete_student(self, student_id: str) -> bool:
        try:
            result = self.student_repo.collection.delete_one({"student_id": student_id})
            # Also deactivate their RFIDs
            self.rfid_repo.collection.update_many({"student_id": student_id}, {"$set": {"is_active": False}})
            return result.deleted_count > 0
        except Exception:
            return False

    def assign_rfid(self, student_id: str, uid: str) -> bool:
        normalized_uid = normalize_uid(uid)
        
        # Check if active anywhere
        existing_card = self.rfid_repo.get_active_by_uid(normalized_uid)
        if existing_card and existing_card["student_id"] != student_id:
            raise ValueError(f"RFID card is already assigned to student {existing_card['student_id']}")
            
        # Deactivate old cards for this student
        self.rfid_repo.collection.update_many(
            {"student_id": student_id},
            {"$set": {"is_active": False}}
        )
        
        # Assign new
        from datetime import datetime, timezone
        self.rfid_repo.insert_one({
            "uid": normalized_uid,
            "student_id": student_id,
            "is_active": True,
            "assigned_at": datetime.now(timezone.utc)
        })
        return True