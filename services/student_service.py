from repositories import (
    StudentRepository,
    ParentRepository,
    RFIDRepository
)

from schemas.student_schema import StudentOut
from utils.id_utils import normalize_uid


class StudentService:

    def __init__(self):
        self.student_repo = StudentRepository()
        self.parent_repo = ParentRepository()
        self.rfid_repo = RFIDRepository()

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
