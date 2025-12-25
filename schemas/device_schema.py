from pydantic import BaseModel, Field
from typing import Optional


class DeviceBase(BaseModel):
    device_id: str
    location_name: str
    is_active: bool = True
    last_seen: Optional[str] = None
