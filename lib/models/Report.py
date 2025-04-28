from fastapi import APIRouter
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from config import Base  # Assuming you have your Base defined in config.py

class Report(Base):
    __tablename__ = "report"

    id = Column(String, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=True)
    content = Column(String, nullable=True)