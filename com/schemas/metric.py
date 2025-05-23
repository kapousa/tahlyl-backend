import datetime
from typing import Optional

from pydantic import BaseModel


class MetricSchema(BaseModel):
    id: str
    name: Optional[str] = None
    value: Optional[str] = None
    unit: Optional[str] = None
    reference_range_min: Optional[str] = None
    reference_range_max: Optional[str] = None
    status: Optional[str] = None
    report_id: str
    result_id: str
    created_by: Optional[str] = None
    created_date: Optional[datetime.datetime] = None
    updated_by: Optional[str] = None
    updated_date: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


class MetricCreate(BaseModel):
    pass

    class Config:
        orm_mode = True


class MetricUpdate(BaseModel):
    pass

    class Config:
        orm_mode = True
