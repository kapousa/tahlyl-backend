from sqlalchemy import Column, String
from config import Base

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, unique=False, nullable=True)
    avatar = Column(String, unique=True, nullable=False)