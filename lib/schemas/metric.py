import datetime
from typing import Optional

from pydantic import BaseModel


class MetricSchema(BaseModel):
    id: int
    name: str
    value: float
    unit: str
    referenceRangeMin: Optional[float] = None
    referenceRangeMax: Optional[float] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    created_date: Optional[datetime.datetime] = None
    updated_by: Optional[str] = None
    updated_date: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


class MetricUpdateSchema(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    referenceRangeMin: Optional[float] = None
    referenceRangeMax: Optional[float] = None
    status: Optional[str] = None
    updated_by: Optional[str] = None
    updated_date: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True
