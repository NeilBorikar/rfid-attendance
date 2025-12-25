import time
from workers.notification_worker import NotificationWorker
from workers.attendance_worker import AttendanceWorker


def start_scheduler():
    notification_worker = NotificationWorker()
    attendance_worker = AttendanceWorker()

    while True:
        # Retry failed WhatsApp messages
        notification_worker.resend_notification_batch()

        # Reprocess failed attendance
        attendance_worker.reprocess_pending_events()

        time.sleep(60)  # run every minute
