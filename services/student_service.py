from typing import List, Optional
from sqlalchemy.orm import Session

from models.student import Student
from models.parent import Parent
from models.rfid_card import RFIDCard

from repositories.student_repository import StudentRepository
from repositories.parent_repository import ParentRepository
from repositories.rfid_repository import RFIDRepository


class StudentService:
    """
    Backend service responsible for:
    - Resolving RFID UID to Student
    - Validating student status
    - Fetching parent contact details
    """

    def __init__(self, db: Session):
        self.db = db
        self.student_repo = StudentRepository(db)
        self.parent_repo = ParentRepository(db)
        self.rfid_repo = RFIDRepository(db)

    # ==================================================
    # CORE IDENTITY RESOLUTION
    # ==================================================

    def resolve_student_by_uid(self, uid: str) -> Optional[Student]:
        """
        Resolve an RFID UID into an active Student.

        Returns:
            Student object if valid and active
            None if UID is invalid, revoked, or student inactive
        """

        # Step 1: Find active RFID card
        rfid_card: RFIDCard = self.rfid_repo.get_active_by_uid(uid)
        if not rfid_card:
            return None

        # Step 2: Find student linked to RFID card
        student: Student = self.student_repo.get_by_id(rfid_card.student_id)
        if not student or not student.is_active:
            return None

        return student

    # ==================================================
    # PARENT LOOKUPS
    # ==================================================

    def get_parents(self, student_id: int) -> List[Parent]:
        """
        Fetch all parents linked to a student.
        """
        return self.parent_repo.get_by_student_id(student_id)

    def get_whatsapp_enabled_parents(self, student_id: int) -> List[Parent]:
        """
        Fetch only parents who have WhatsApp notifications enabled.
        """
        parents = self.get_parents(student_id)
        return [parent for parent in parents if parent.whatsapp_enabled]

    # ==================================================
    # VALIDATION HELPERS
    # ==================================================

    def is_valid_student_uid(self, uid: str) -> bool:
        """
        Check whether a UID belongs to a valid, active student.
        """
        return self.resolve_student_by_uid(uid) is not None
