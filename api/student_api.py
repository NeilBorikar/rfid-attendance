from fastapi import APIRouter, HTTPException, status, Depends
from services.student_service import StudentService
from schemas.student_schema import StudentCreate, StudentOut
from api.auth_api import get_current_admin

router = APIRouter(tags=["Students"])
student_service = StudentService()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=StudentOut,
    summary="Register a new student",
    dependencies=[Depends(get_current_admin)]
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

from pydantic import BaseModel

class RFIDAssignRequest(BaseModel):
    uid: str

@router.get(
    "/",
    response_model=list[StudentOut],
    summary="Get all students",
    dependencies=[Depends(get_current_admin)]
)
def get_all_students():
    return student_service.get_all_students()

@router.delete(
    "/{student_id}",
    summary="Delete a student",
    dependencies=[Depends(get_current_admin)]
)
def delete_student(student_id: str):
    success = student_service.delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted"}

@router.patch(
    "/{student_id}/rfid",
    summary="Assign RFID to student",
    dependencies=[Depends(get_current_admin)]
)
def assign_rfid(student_id: str, request: RFIDAssignRequest):
    try:
        student_service.assign_rfid(student_id, request.uid)
        return {"detail": "RFID assigned successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
