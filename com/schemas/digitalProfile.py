from pydantic import BaseModel, Field
from typing import Optional

class DigitalProfileBase(BaseModel):
    health_overview: Optional[str] = None
    recommendations: Optional[str] = None
    attention_points: Optional[str] = None
    risks: Optional[str] = None
    creation_date: Optional[str] = None

class DigitalProfileCreate(DigitalProfileBase):
    pass

class DigitalProfile(DigitalProfileBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True