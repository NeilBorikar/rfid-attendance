from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =========================
# BASE DEVICE SCHEMA
# =========================
class DeviceBase(BaseModel):
    """
    Core device identity & status.
    Shared across backend layers.
    """
    device_id: str = Field(..., example="SCHOOL_GATE_1")
    location_name: str = Field(..., example="Main Gate")
    is_active: bool = Field(default=True)

    last_seen_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# =========================
# DEVICE CONFIG (ESP RESPONSE)
# =========================
class DeviceConfigResponse(DeviceBase):
    """
    Configuration sent to ESP device.
    ESP pulls this periodically.
    """
    wifi_ssid: str
    wifi_password: str


# =========================
# DEVICE CONFIG (APP UPDATE)
# =========================
class DeviceConfigUpdate(BaseModel):
    """
    Configuration updates coming from admin/app.
    """
    wifi_ssid: Optional[str] = None
    wifi_password: Optional[str] = None
    is_active: Optional[bool] = None


# =========================
# DEVICE CREATE (OPTIONAL / FUTURE)
# =========================
class DeviceCreate(DeviceBase):
    """
    Used when registering a new device.
    """
    wifi_ssid: str
    wifi_password: str
