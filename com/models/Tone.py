from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from config import Base  # Assuming you have your Base defined in config.py

class Tone(Base):
    __tablename__ = "tone"

    id = Column(String, primary_key=True, unique=True, nullable=False)
    tone = Column(String, unique=True, nullable=False)

    results = relationship("Result", back_populates="tone")