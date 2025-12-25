from workers.base_worker import BaseWorker
from services.attendance_service import AttendanceService
from repositories.attendance_repository import AttendanceRepository


class AttendanceWorker(BaseWorker):

    def __init__(self):
        self.attendance_service = AttendanceService()
        self.attendance_repo = AttendanceRepository()

    def reprocess_pending_events(self):
        pending_events = self.attendance_repo.get_pending_events()

        for event in pending_events:
            self.run_with_retry(
                self.attendance_service.process_event,
                event
            )

            self.attendance_repo.mark_processed(event["_id"])
