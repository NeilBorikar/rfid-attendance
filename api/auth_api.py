from fastapi import APIRouter, HTTPException, status, Depends
from services.auth_service import AuthService
from schemas.user_schema import UserCreate, Token, LoginRequest
import jwt
from app.settings import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
auth_service = AuthService()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return user

def get_current_admin_or_teacher(user: dict = Depends(get_current_user)):
    if user.get("role") not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return user

@router.post("/login", response_model=Token, summary="Login")
def login(request: LoginRequest):
    user = auth_service.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "role": user.role, "name": user.name, "id": user.id}
    )
    return {"token": access_token, "user": user}

@router.post("/admin/register", summary="Register Admin (Backend Only)")
def register_admin(user: UserCreate):
    """
    Unprotected route to create an initial admin or backend-only usage.
    """
    user.role = "admin"
    try:
        return auth_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
