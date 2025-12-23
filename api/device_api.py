from fastapi import APIRouter, HTTPException, status
from services.device_service import DeviceService
from schemas.device_schema import DeviceSchema

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def register_device(device: DeviceSchema):
    device_service = DeviceService()

    try:
        device_service.register_device(device.dict())
        return {"message": "Device registered successfully"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
