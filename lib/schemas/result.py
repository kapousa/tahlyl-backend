from pydantic import BaseModel
from typing import Optional

class ResultBase(BaseModel):
    result: str
    tone_id: Optional[str] = None
    report_id: str

class ResultCreate(ResultBase):
    pass

class ResultUpdate(ResultBase):
    pass

class Result(ResultBase):
    id: str

    class Config:
        orm_mode = True