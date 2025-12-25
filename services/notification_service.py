from repositories import NotificationRepository
from services.student_service import StudentService
from notifications.whatsapp_client import WhatsAppClient

from schemas.notification_schema import NotificationLog
from utils.message_utils import build_attendance_message
from utils.time_utils import utc_now


class NotificationService:

    def __init__(self):
        self.student_service = StudentService()
        self.notification_repo = NotificationRepository()
        self.whatsapp_client = WhatsAppClient()

    def notify_parents(self, student, event_type, event_time, device):
        parents = self.student_service.get_whatsapp_enabled_parents(
            student["student_id"]
        )

        for parent in parents:
            # 1️⃣ Build message using utils (no formatting logic here)
            message = build_attendance_message(
                student_name=student["full_name"],
                event_type=event_type,
                event_time=event_time,
                location=device["location_name"]
            )

            # 2️⃣ Send WhatsApp message
            self.whatsapp_client.send_message(
                to=parent["phone_number"],
                message=message
            )

            # 3️⃣ Log notification using schema
            notification_log = NotificationLog(
                student_id=student["student_id"],
                parent_phone=parent["phone_number"],
                event_type=event_type,
                status="SENT",
                sent_at=utc_now()
            )

            self.notification_repo.log_notification(
                notification_log.dict()
            )
