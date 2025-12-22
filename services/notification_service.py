from datetime import datetime
from notifications.whatsapp_client import WhatsAppClient
from notifications.message_template import entry_message, exit_message

class NotificationService:

    def __init__(self):
        self.whatsapp = WhatsAppClient()

    def notify_parents(
        self, 
        parents: list,
        student_name: str,
        event_type: str,
        event_time: datetime,
        device_name: str
    ):
        for parent in parents:
            if not parent.whatsapp_enabled:
                continue

            if event_type == "IN":
                message = entry_message(student_name, event_time, device_name)
            elif event_type == "OUT":
                message = exit_message(student_name, event_time, device_name)
            else:
                return

            try:
                self.whatsapp.send_message(
                    to=parent.phone_number,
                    message=message
                )
            except Exception as e:
                # log failure (DB / logger later)
                print(f"WhatsApp failed for {parent.phone_number}: {e}")
