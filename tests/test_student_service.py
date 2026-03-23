from services.student_service import StudentService
from schemas.student_schema import StudentCreate


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


def test_register_student(mocker):
    service = StudentService()

    # Mock repository methods
    service.student_repo.get_by_student_id = mocker.Mock(return_value=None)
    service.student_repo.insert_one = mocker.Mock(return_value="new_id")

    student_data = StudentCreate(
        student_id="STU123",
        full_name="John Doe",
        grade="10",
        section="A"
    )

    result = service.register_student(student_data)

    assert result.student_id == "STU123"
    assert result.full_name == "John Doe"
    service.student_repo.insert_one.assert_called_once()
