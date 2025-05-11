from datetime import datetime

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from config import Base  # Assuming you have your Base defined in config.py

class Result(Base):
    __tablename__ = "result"

    id = Column(String, primary_key=True, unique=True, nullable=False)
    result = Column(Text, nullable=False)
    tone_id = Column(String, ForeignKey("tone.id"), nullable=True)
    language = Column(Text, nullable=True)
    report_id = Column(String, ForeignKey("report.id"), nullable=False)
    added_datetime = Column(String, default=lambda: datetime.now().isoformat())
