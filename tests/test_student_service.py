from services.student_service import StudentService


def test_resolve_student_by_uid(mocker):
    service = StudentService()

    service.rfid_repo.get_active_by_uid = mocker.Mock(
        return_value={"student_id": "S1"}
    )
    service.student_repo.get_by_student_id = mocker.Mock(
        return_value={"student_id": "S1", "full_name": "John"}
    )

    student = service.resolve_student_by_uid("AA-BB")

    assert student.student_id == "S1"
