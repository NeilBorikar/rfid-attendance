from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    role: str = Field(default="teacher", description="Role of the user: 'admin' or 'teacher'")

class UserInDB(BaseModel):
    email: str
    name: str
    role: str
    hashed_password: str

class UserOut(BaseModel):
    id: str
    email: str
    name: str
    role: str

class Token(BaseModel):
    token: str
    user: UserOut

class LoginRequest(BaseModel):
    email: str
    password: str
