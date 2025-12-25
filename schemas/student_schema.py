from pydantic import BaseModel, Field
from typing import Optional


class StudentBase(BaseModel):
    student_id: str = Field(..., description="Unique student ID")
    full_name: str
    grade: str
    section: Optional[str] = None
    is_active: bool = True


class StudentOut(StudentBase):
    pass
