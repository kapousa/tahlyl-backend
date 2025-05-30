from datetime import datetime

from fastapi import APIRouter
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from config import Base  # Assuming you have your Base defined in config.py

class Report(Base):
    __tablename__ = "report"

    id = Column(String, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    user_id = Column(String)
    content = Column(String, nullable=True)
    status = Column(String, nullable=True)
    report_type = Column(String, nullable=True)
    added_datetime = Column(String, default=lambda: datetime.now().isoformat())

    results = relationship("Result", back_populates="report")
