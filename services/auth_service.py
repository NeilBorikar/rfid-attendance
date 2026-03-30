from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from app.settings import settings
from core.database import MongoDB
from schemas.user_schema import UserCreate, UserInDB, UserOut
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt", "bcrypt_sha256"], deprecated="auto")
ALGORITHM = "HS256"

class AuthService:
    def __init__(self):
        self.db = MongoDB.get_database()
        self.collection = self.db["users"]

    def get_password_hash(self, password: str) -> str:
        print(f"DEBUG: Hashing password of length {len(password)}")
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def create_user(self, user_in: UserCreate) -> UserOut:
        # Check if user already exists
        if self.collection.find_one({"email": user_in.email}):
            raise ValueError("User with this email already exists")

        # Create new user
        hashed_password = self.get_password_hash(user_in.password)
        db_user = UserInDB(
            email=user_in.email,
            name=user_in.name,
            role=user_in.role,
            hashed_password=hashed_password
        )
        
        result = self.collection.insert_one(db_user.model_dump())
        
        return UserOut(
            id=str(result.inserted_id),
            email=db_user.email,
            name=db_user.name,
            role=db_user.role
        )

    def authenticate_user(self, email: str, password: str):
        user = self.collection.find_one({"email": email})
        if not user:
            return None
        if not self.verify_password(password, user["hashed_password"]):
            return None
        
        return UserOut(
            id=str(user["_id"]),
            email=user["email"],
            name=user["name"],
            role=user["role"]
        )
