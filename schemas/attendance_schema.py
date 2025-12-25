from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class AttendanceEventIn(BaseModel):
    uid: str = Field(
        ...,
        description="RFID card UID"
    )
    status: Literal["IN", "OUT"] = Field(
        ...,
        description="Attendance type"
    )
    device_id: str = Field(
        ...,
        description="Device identifier"
    )
    timestamp: float = Field(
        ...,
        description="Unix timestamp from device"
    )


class AttendanceEventOut(BaseModel):
    student_id: str
    uid: str
    status: str
    device_id: str
    event_time: datetime
