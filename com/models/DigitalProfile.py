# com/models/DigitalProfile.py

from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.orm import relationship
from config import Base # Assuming you have a Base object from your SQLAlchemy setup
import com.models.User as User

class DigitalProfile(Base):
    __tablename__ = "digital_profile"

    id = Column(Text, primary_key=True, unique=True, nullable=False)
    health_overview = Column(Text)
    recommendations = Column(Text)
    attention_points = Column(Text)
    risks = Column(Text)
    creation_date = Column(Text)
    user_id = Column(Text, ForeignKey("user.id"))

    user = relationship("User", back_populates="digital_profile")