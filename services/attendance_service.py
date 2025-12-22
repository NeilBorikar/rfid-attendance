from datetime import datetime
from sqlalchemy.orm import Session

from repositories.attendance_repository import AttendanceRepository
from repositories.device_repository import DeviceRepository
from services.student_service import StudentService
from services.notification_service import NotificationService


class AttendanceService:
    """
    Core backend service for handling attendance events.
    """

    def __init__(self, db: Session):
        self.db = db
        self.attendance_repo = AttendanceRepository(db)
        self.device_repo = DeviceRepository(db)
        self.student_service = StudentService(db)
        self.notification_service = NotificationService()

    # --------------------------------------------------
    # MAIN ENTRY POINT
    # --------------------------------------------------

    def process_event(self, event: dict):
        """
        Process a raw attendance event received from ESP32.
        """

        uid = event.get("uid")
        event_type = event.get("status")
        device_id = event.get("device_id")
        timestamp = event.get("timestamp")

        # -------------------------------
        # 1️⃣ Validate basic payload
        # -------------------------------
        if not uid or event_type not in ("IN", "OUT") or not device_id or not timestamp:
            raise ValueError("Invalid attendance payload")

        # -------------------------------
        # 2️⃣ Verify device
        # -------------------------------
        device = self.device_repo.get_by_device_id(device_id)
        if not device or not device.is_active:
            raise PermissionError("Unauthorized or inactive device")

        # -------------------------------
        # 3️⃣ Resolve student
        # -------------------------------
        student = self.student_service.resolve_student_by_uid(uid)
        if not student:
            raise ValueError("Invalid or inactive RFID card")

        # -------------------------------
        # 4️⃣ Convert timestamp
        # -------------------------------
        event_time = datetime.fromtimestamp(timestamp)

        # -------------------------------
        # 5️⃣ Prevent duplicate events
        # -------------------------------
        if self.attendance_repo.event_exists(
            uid=uid,
            device_id=device.id,
            event_time=event_time,
            event_type=event_type,
        ):
            # Duplicate replay from offline ESP32 → ignore safely
            return {"status": "duplicate_ignored"}

        # -------------------------------
        # 6️⃣ Save attendance event
        # -------------------------------
        attendance_event = self.attendance_repo.create_event(
            uid=uid,
            student_id=student.id,
            device_id=device.id,
            event_type=event_type,
            event_timestamp=event_time,
        )

        # -------------------------------
        # 7️⃣ Trigger notification
        # -------------------------------
        parents = self.student_service.get_whatsapp_enabled_parents(student.id)

        self.notification_service.notify_parents(
            parents=parents,
            student_name=student.full_name,
            event_type=event_type,
            event_time=event_time,
            device_name=device.location_name,
        )

        # -------------------------------
        # 8️⃣ Return success
        # -------------------------------
        return {
            "status": "success",
            "event_id": attendance_event.id,
            "student_id": student.id,
        }
