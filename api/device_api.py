from fastapi import APIRouter, HTTPException, status, Header
from typing import Optional

from services.device_service import DeviceService
from schemas.device_schema import (
    DeviceBase,
    DeviceConfigResponse,
    DeviceConfigUpdate
)

router = APIRouter(prefix="/devices", tags=["Devices"])

device_service = DeviceService()

# =========================
# ADMIN APIs
# =========================

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Register new ESP device"
)
def register_device(device: DeviceBase):
    """
    Register a new ESP device (admin/app).
    """

    try:
        return device_service.register_device(device)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put(
    "/{device_id}/config",
    summary="Update device configuration (Wi-Fi, status)"
)
def update_device_config(
    device_id: str,
    config: DeviceConfigUpdate
):
    """
    Update device configuration from admin/app.
    """

    try:
        return device_service.update_device_config(
            device_id=device_id,
            update_data=config
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# =========================
# DEVICE (ESP) APIs
# =========================

@router.get(
    "/config",
    response_model=DeviceConfigResponse,
    summary="Fetch device configuration (ESP)"
)
def fetch_device_config(
    device_id: Optional[str] = Header(None, alias="Device-ID")
):
    """
    ESP firmware pulls latest configuration.
    """

    if not device_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device-ID header missing"
        )

    try:
        return device_service.get_device_config(device_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
