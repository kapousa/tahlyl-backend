import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from config import Base


class Metric(Base):
    __tablename__ = "metric"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    reference_range_min = Column(String, nullable=True)
    reference_range_max = Column(String, nullable=True)
    status = Column(String, nullable=True)
    report_id = Column(String, ForeignKey("report.id"), nullable=False)
    result_id = Column(String, ForeignKey("result.id"), nullable=False)
    created_by = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_by = Column(String, nullable=True)
    updated_date = Column(DateTime, nullable=True)


