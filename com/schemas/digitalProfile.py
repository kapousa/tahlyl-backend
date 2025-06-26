from pydantic import BaseModel, Field
from typing import Optional, Union, Dict, List


class DigitalProfileBase(BaseModel):
    health_overview: Optional[Union[str, Dict, List]] = None
    recommendations: Optional[Union[str, Dict, List]] = None
    attention_points: Optional[Union[str, Dict, List]] = None
    risks: Optional[Union[str, Dict, List]] = None
    creation_date: Optional[str] = None
    recent: int

class DigitalProfileCreate(DigitalProfileBase):
    pass

class DigitalProfile(DigitalProfileBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True