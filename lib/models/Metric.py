import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from lib.schemas.bloodTest import Base


class Metric(Base):
    __tablename__ = "metric"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bloodTestId = Column(String(255), ForeignKey("blood_test.id"), nullable=False)
    name = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    referenceRangeMin = Column(Float, nullable=True)
    referenceRangeMax = Column(Float, nullable=True)
    status = Column(String(50), nullable=True)
    created_by = Column(String(255), nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_by = Column(String(255), nullable=True)
    updated_date = Column(DateTime, nullable=True)

    blood_test = relationship("BloodTest", back_populates="metrics")
