# com/models/User.py (Your User SQLAlchemy model)

from sqlalchemy import Column, String # Assuming String for ID, adjust if Integer
from sqlalchemy.orm import relationship
# Make sure this import path is correct for your project structure
from com.models.Role import user_roles_association
from config import Base # Your declarative_base

class User(Base):
    __tablename__ = "user" # Keep as "user" as per your existing design

    id = Column(String, primary_key=True, index=True) # Assuming UUIDs as strings for IDs
    username = Column(String(25), unique=True, nullable=False)
    password = Column(String, nullable=False) # This should be hashed_password, not plain password
    email = Column(String, unique=True, nullable=False)
    avatar = Column(String, nullable=True)

    # SQLAlchemy ORM-managed relationship (collection_class=set is correct here)
    roles = relationship(
        "Role",
        secondary=user_roles_association,
        back_populates="users",
        collection_class=set
    )

    # --- NEW: Non-database-mapped attribute for roles from token ---
    # This attribute will temporarily hold the list of role names from the JWT.
    # It is not a database column; it's a Python-only attribute that we set
    # after fetching the user from the DB.
    roles_from_token: list[str] = []

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"