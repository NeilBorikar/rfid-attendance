from fastapi import APIRouter, HTTPException, Depends
from schemas.user_schema import UserCreate, UserOut
from services.auth_service import AuthService
from api.auth_api import get_current_admin

router = APIRouter()
auth_service = AuthService()

@router.post("/register", response_model=UserOut, summary="Register Teacher")
def register_teacher(user: UserCreate, current_admin: dict = Depends(get_current_admin)):
    """
    Register a new teacher. Only an admin can perform this action.
    """
    user.role = "teacher"
    try:
        return auth_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
