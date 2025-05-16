from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Float, Text

from config import Base


class APILog(Base):
    __tablename__ = "api_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    method = Column(String)
    path = Column(String)
    status_code = Column(Integer)
    duration = Column(Float)
    user_id = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    traceback = Column(Text, nullable=True)
