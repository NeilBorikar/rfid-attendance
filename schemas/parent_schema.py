from pydantic import BaseModel, Field


class ParentBase(BaseModel):
    parent_id: str
    student_id: str
    name: str
    phone_number: str = Field(
        ...,
        description="WhatsApp-enabled phone number"
    )
    whatsapp_enabled: bool = True
