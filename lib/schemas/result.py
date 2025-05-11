from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

class ResultBase(BaseModel):
    result: str
    tone_id: Optional[str] = None
    language: Optional[str] = None
    report_id: str
    added_datetime: str = Field(default_factory=lambda: datetime.now().isoformat())


    class Config:
        from_attributes = True

class ResultCreate(ResultBase):
    pass

class ResultUpdate(ResultBase):
    pass

class Result(ResultBase):
    id: str

    class Config:
        orm_mode = True