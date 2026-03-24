from fastapi import APIRouter

from api.attendance_api import router as attendance_router
from api.device_api import router as device_router
from api.health_api import router as health_router
from api.student_api import router as student_router
from api.auth_api import router as auth_router
from api.teacher_api import router as teacher_router


api_router = APIRouter()

api_router.include_router(
    attendance_router,
    prefix="/attendance",
    tags=["Attendance"]
)

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
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

api_router.include_router(
    student_router,
    prefix="/students",
    tags=["Students"]
)

api_router.include_router(
    teacher_router,
    prefix="/teachers",
    tags=["Teachers"]
)
