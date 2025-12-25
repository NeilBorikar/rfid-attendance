from datetime import datetime

from repositories import (
    AttendanceRepository,
    DeviceRepository,
    RFIDRepository
)
from services.student_service import StudentService
from services.notification_service import NotificationService

from schemas.attendance_schema import AttendanceEventIn
from utils.time_utils import unix_to_utc_datetime
from utils.id_utils import normalize_uid, normalize_device_id


class AttendanceService:

    def __init__(self):
        self.attendance_repo = AttendanceRepository()
        self.device_repo = DeviceRepository()
        self.rfid_repo = RFIDRepository()
        self.student_service = StudentService()
        self.notification_service = NotificationService()

    def process_event(self, event: AttendanceEventIn):
        """
        Main attendance processing pipeline.
        """

        # 1️⃣ Normalize & trust validated data
        uid = normalize_uid(event.uid)
        device_id = normalize_device_id(event.device_id)
        event_type = event.status
        event_time = unix_to_utc_datetime(event.timestamp)

        # 2️⃣ Validate device
        device = self.device_repo.get_active_device(device_id)
        if not device:
            raise ValueError("Invalid or inactive device")

        self.device_repo.update_last_seen(device_id)

        # 3️⃣ Resolve student via RFID
        student = self.student_service.resolve_student_by_uid(uid)
        if not student:
            raise ValueError("Invalid RFID or inactive student")

        # 4️⃣ Prevent duplicate attendance
        if self.attendance_repo.event_exists(uid, event_type, event_time):
            return  # silently ignore duplicate

        # 5️⃣ Store attendance event
        attendance_event = {
            "uid": uid,
            "student_id": student["student_id"],
            "device_id": device_id,
            "event_type": event_type,
            "event_time": event_time
        }

        self.attendance_repo.create_event(attendance_event)

        # 6️⃣ Trigger notifications
        self.notification_service.notify_parents(
            student=student,
            event_type=event_type,
            event_time=event_time,
            device=device
        )
