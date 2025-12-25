from services.notification_service import NotificationService


def test_notify_parents(mocker):
    service = NotificationService()

    service.student_service.get_whatsapp_enabled_parents = mocker.Mock(
        return_value=[{"phone_number": "9999999999"}]
    )
    service.whatsapp_client.send_message = mocker.Mock()
    service.notification_repo.log_notification = mocker.Mock()

    service.notify_parents(
        student={"student_id": "S1", "full_name": "John"},
        event_type="IN",
        event_time=mocker.Mock(),
        device={"location_name": "Gate 1"}
    )

    service.whatsapp_client.send_message.assert_called_once()
