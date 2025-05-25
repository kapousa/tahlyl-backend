from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional, List

from com.schemas.metric import MetricSchema as Metric


class ReportBase(BaseModel):
    name: str
    location: Optional[str] = None
    content: Optional[str] = None
    report_type: Optional[str] = None
    status: Optional[str] = None
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


class ReportCard(BaseModel):
    id: str
    name: str
    added_datetime: str
    status: str
    metrics: List[Metric]

    class Config:
        orm_mode = True