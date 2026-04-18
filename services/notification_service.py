from repositories import NotificationRepository
from services.student_service import StudentService
from notifications.whatsapp_client import WhatsAppClient
from notifications.sms_client import SMSClient

from schemas.notification_schema import NotificationLog
from utils.message_utils import build_attendance_message
from utils.time_utils import utc_now


class NotificationService:

    def __init__(self):
        self.student_service = StudentService()
        self.notification_repo = NotificationRepository()
        self.whatsapp_client = WhatsAppClient()
        self.sms_client = SMSClient()

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

    def send_manual_sms(self, student_id: str, message: str):
        """
        Send a manual SMS to parents for a specific student.
        """
        parents = self.student_service.parent_repo.get_by_student_id(student_id)
        
        results = []
        for parent in parents:
            phone_number = parent.get("phone_number")
            if not phone_number:
                continue
                
            res = self.sms_client.send_sms(to=phone_number, message=message)
            
            # Log notification
            notification_log = NotificationLog(
                student_id=student_id,
                parent_phone=phone_number,
                event_type="MANUAL_SMS",
                status="SENT" if res["status"] == "success" else "FAILED",
                sent_at=utc_now()
            )
            self.notification_repo.log_notification(notification_log.dict())
            results.append(res)
            
        return results
