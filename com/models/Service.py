from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    category_id = Column(String, ForeignKey("category.id"))  # Assuming category table exists
    url = Column(String)
    beneficiary_id = Column(String, ForeignKey("beneficiary.id")) # Assuming beneficiary table exists
    keyAICapabilities = Column(Text)
    icon = Column(Text)

    # Optional: Relationships (assuming you have Category and Beneficiary models)
    # category = relationship("Category", back_populates="services")
    # beneficiary = relationship("Beneficiary", back_populates="services")