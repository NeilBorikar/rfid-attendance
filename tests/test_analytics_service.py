from services.analytics_service import AnalyticsService


def test_get_student_events(mocker):
    service = AnalyticsService()
    service.attendance_repo.find_many = mocker.Mock(
        return_value=[
            {
                "student_id": "S1",
                "uid": "AA",
                "status": "IN",
                "device_id": "G1",
                "event_time": mocker.Mock()
            }
        ]
    )

    events = service.get_student_events("S1")

    assert len(events) == 1
