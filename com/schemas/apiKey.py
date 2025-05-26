import json
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_serializer 


class APIKeyBase(BaseModel):
    client_name: str
    permissions: List[str] = Field(default_factory=list) # Default to empty list

class APIKeyCreate(APIKeyBase):
    # For creation, permissions are passed as a list
    pass

class APIKeyResponse(APIKeyBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    api_key_plain_text: Optional[str] = None # ONLY returned on creation

    class Config:
        # For Pydantic V2, use `from_attributes = True`
        from_attributes = True
        # For Pydantic V1, use `orm_mode = True`
        # orm_mode = True

    # Pydantic v2: Custom serializer for permissions if they were loaded from DB as a string
    # This ensures `permissions` field in Pydantic model is always a list
    @field_serializer('permissions')
    def serialize_permissions_list(self, permissions: List[str]) -> List[str]:
        # This will be called when converting APIKeyResponse back to JSON
        return permissions
