import datetime

from sqlalchemy import Column, String, Date, Text, DateTime
from sqlalchemy.orm import relationship

from com.schemas.bloodTest import Base


class BloodTest(Base):
    __tablename__ = "blood_test"

    id = Column(String(255), primary_key=True)
    date = Column(Date, nullable=False)
    name = Column(String(255), nullable=False)
    fileUrl = Column(Text, nullable=True)
    status = Column(String(50), nullable=True)
    created_by = Column(String(255), nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_by = Column(String(255), nullable=True)
    updated_date = Column(DateTime, nullable=True)
    content = Column(Text, nullable=True)  # Added content column
