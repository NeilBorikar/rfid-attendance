from fastapi import APIRouter, HTTPException, status
from schemas.attendance_schema import AttendanceEventSchema
from services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def record_attendance(event: AttendanceEventSchema):
    """
    Endpoint called by ESP32 devices to record attendance.
    """

    attendance_service = AttendanceService()

    try:
        attendance_service.process_event(event.dict())
        return {"message": "Attendance recorded successfully"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
