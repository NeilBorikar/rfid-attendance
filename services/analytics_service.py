from repositories import AttendanceRepository
from schemas.attendance_schema import AttendanceEventOut


class AnalyticsService:

    def __init__(self):
        self.attendance_repo = AttendanceRepository()

    def get_student_events(self, student_id: str):
        """
        Fetch all attendance events for a student.
        """

        events = self.attendance_repo.find_many({
            "student_id": student_id
        })

        # Return schema-backed, structured events
        return [AttendanceEventOut(**event) for event in events]
