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

@router.get("/", response_model=list[UserOut], summary="Get All Teachers")
def get_all_teachers(current_admin: dict = Depends(get_current_admin)):
    """
    Retrieve all registered teachers. Only an admin can perform this action.
    """
    return auth_service.get_users_by_role("teacher")

@router.delete("/{teacher_id}", summary="Delete Teacher")
def delete_teacher(teacher_id: str, current_admin: dict = Depends(get_current_admin)):
    """
    Delete a teacher by ID. Only an admin can perform this action.
    """
    success = auth_service.delete_user(teacher_id)
    if not success:
        raise HTTPException(status_code=404, detail="Teacher not found or invalid ID")
    return {"detail": "Teacher deleted successfully"}
