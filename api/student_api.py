from fastapi import APIRouter, HTTPException, status
from services.student_service import StudentService
from schemas.student_schema import StudentCreate, StudentOut

router = APIRouter(tags=["Students"])
student_service = StudentService()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=StudentOut,
    summary="Register a new student"
)
def register_student(student: StudentCreate):
    """
    Register a new student in the system.
    """
    try:
        return student_service.register_student(student)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
