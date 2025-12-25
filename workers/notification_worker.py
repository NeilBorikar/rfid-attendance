from workers.base_worker import BaseWorker
from notifications.whatsapp_client import WhatsAppClient
from repositories.notification_repository import NotificationRepository
from utils.time_utils import utc_now


class NotificationWorker(BaseWorker):

    def __init__(self):
        self.whatsapp_client = WhatsAppClient()
        self.notification_repo = NotificationRepository()

    def resend_notification(self, notification_log: dict):
        """
        Retry sending WhatsApp notification.
        """

        def task():
            self.whatsapp_client.send_message(
                to=notification_log["parent_phone"],
                message=notification_log["message"]
            )

            self.notification_repo.update_status(
                notification_log["_id"],
                status="SENT",
                sent_at=utc_now()
            )

        self.run_with_retry(task)
