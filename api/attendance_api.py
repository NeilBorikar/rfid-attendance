from fastapi import APIRouter, HTTPException, status, Header
from typing import Optional

from schemas.attendance_schema import AttendanceEventIn
from services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance"])

attendance_service = AttendanceService()


@router.post(
    "/event",
    status_code=status.HTTP_200_OK,
    summary="Record attendance event (ESP)"
)
def record_attendance(
    event: AttendanceEventIn,
    device_id: Optional[str] = Header(None, alias="Device-ID")
):
    """
    Endpoint called by ESP devices to submit attendance events.
    """

    if not device_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device-ID header missing"
        )

    try:
        # Merge header-level device identity into event
        event_data = event.dict()
        event_data["device_id"] = device_id

        attendance_service.process_event(event_data)

        return {
            "status": "accepted"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
