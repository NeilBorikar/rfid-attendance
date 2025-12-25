from pydantic import BaseModel
from datetime import datetime


class NotificationLog(BaseModel):
    student_id: str
    parent_phone: str
    event_type: str
    status: str
    sent_at: datetime
