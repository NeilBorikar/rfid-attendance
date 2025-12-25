from fastapi import APIRouter

from api.attendance_api import router as attendance_router
from api.device_api import router as device_router
from api.health_api import router as health_router


api_router = APIRouter()

api_router.include_router(
    attendance_router,
    prefix="/attendance",
    tags=["Attendance"]
)

api_router.include_router(
    device_router,
    prefix="/devices",
    tags=["Devices"]
)

api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"]
)
