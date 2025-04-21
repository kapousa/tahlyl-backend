# models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from config import Base # Import your declarative base from config.py

class SQLService(Base): # Give it a distinct name or keep as Service if Pydantic is in schemas.py
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, index=True) # Match SQL type
    api_name = Column(Text, nullable=False)            # Match SQL type & constraints
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=False, default="#")
    # Ensure column names match corrected SQL table
    category_id = Column(Text, ForeignKey("lookup.key"), nullable=True)
    beneficiary_id = Column(Text, ForeignKey("lookup.key"), nullable=True)