from typing import List, Optional
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import datetime

from com.schemas.metric import MetricSchema

Base = declarative_base()

# Pydantic Schema for BloodTest
class BloodTestSchema(BaseModel):
    id: str
    date: datetime.date
    name: str
    fileUrl: Optional[str] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    created_date: Optional[datetime.datetime] = None
    updated_by: Optional[str] = None
    updated_date: Optional[datetime.datetime] = None
    content: Optional[str] = None # Added content to schema
    metrics: List[MetricSchema] = []

    class Config:
        orm_mode = True


class BloodTestCreateSchema(BaseModel):
    id: str
    date: datetime.date
    name: str
    fileUrl: Optional[str] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    created_date: Optional[datetime.datetime] = None
    updated_by: Optional[str] = None
    updated_date: Optional[datetime.datetime] = None
    content: Optional[str] = None

    class Config:
        orm_mode = True


class BloodTestUpdateSchema(BaseModel):
    date: Optional[datetime.date] = None
    name: Optional[str] = None
    fileUrl: Optional[str] = None
    status: Optional[str] = None
    updated_by: Optional[str] = None
    updated_date: Optional[datetime.datetime] = None
    content: Optional[str] = None

    class Config:
        orm_mode = True
