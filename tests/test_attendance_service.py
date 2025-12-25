from services.attendance_service import AttendanceService
from schemas.attendance_schema import AttendanceEventIn


def test_attendance_process_valid_event(mocker):
    service = AttendanceService()

    # Mock dependencies
    service.device_repo.get_active_device = mocker.Mock(
        return_value={"device_id": "GATE_1"}
    )
    service.student_service.resolve_student_by_uid = mocker.Mock(
        return_value={"student_id": "S1", "full_name": "John"}
    )
    service.attendance_repo.event_exists = mocker.Mock(
        return_value=False
    )
    service.attendance_repo.create_event = mocker.Mock()
    service.notification_service.notify_parents = mocker.Mock()

    event = AttendanceEventIn(
        uid="AA-BB",
        status="IN",
        device_id="GATE_1",
        timestamp=123456789
    )

    service.process_event(event)

    service.attendance_repo.create_event.assert_called_once()
    service.notification_service.notify_parents.assert_called_once()
