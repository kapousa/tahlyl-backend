# Service.py (Recommended file name)
from typing import List
from pydantic import BaseModel, ConfigDict  # Import ConfigDict for V2


class ServiceBase(BaseModel):
    # Fields common to creation and reading, without ID
    id: int  # Should be int to match SQL INTEGER
    name: str
    description: str | None = None  # Allow None if description is optional
    url: str | None = None
    category_id: str | None = None  # Assuming TEXT foreign key can be NULL
    beneficiary_id: str | None = None  # Use correct spelling, Assuming TEXT foreign key can be NULL
    keyAICapabilities: str | None = None
    icon: str | None = None

class ServiceCreate(ServiceBase):
    # Use this model for POST/PUT input bodies
    pass

class Service(ServiceBase):
    # This model represents the data returned FROM the API (includes ID)
    id: int  # Should be int to match SQL INTEGER
    name: str
    description: str | None = None  # Allow None if description is optional
    url: str | None = None
    category_id: str | None = None  # Assuming TEXT foreign key can be NULL
    beneficiary_id: str | None = None  # Use correct spelling, Assuming TEXT foreign key can be NULL
    keyAICapabilities: str | None = None
    icon: str | None = None

    # Enable ORM mode for automatic conversion from SQLAlchemy objects
    # Pydantic V2:
    model_config = ConfigDict(from_attributes=True)

    # Pydantic V1:
    # class Config:
    #     orm_mode = True

class ServicesList(BaseModel):
    services: List[Service]
