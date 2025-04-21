from pydantic import BaseModel
from typing import Optional

class ReportBase(BaseModel):
    name: str
    location: Optional[str] = None
    content: Optional[str] = None
    user_id: Optional[str] = None

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    pass

class Report(ReportBase):
    id: str

    class Config:
        orm_mode = True