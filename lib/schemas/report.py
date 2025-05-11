from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

class ReportBase(BaseModel):
    name: str
    location: Optional[str] = None
    content: Optional[str] = None
    user_id: Optional[str] = None
    added_datetime: str = Field(default_factory=lambda: datetime.now().isoformat())


    class Config:
        from_attributes = True

class ReportCreate(ReportBase):
    id: str

class ReportUpdate(ReportBase):
    pass

class Report(ReportBase):
    id: str

    class Config:
        orm_mode = True