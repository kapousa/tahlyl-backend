# com/schemas/client.py (create this new file)

from pydantic import BaseModel
from typing import List, Literal, Optional

class CombinedAuthClient(BaseModel):
    """
    Represents an authenticated client, which can be either a human user or an API Key.
    """
    id: str # User ID or API Key ID
    name: str # Username or Client Name
    client_type: Literal["user", "api_key"] # Distinguishes between human user and API key client

    # User-specific attributes
    roles: List[str] = [] # Roles from JWT payload (for human users)

    # API Key-specific attributes
    permissions: List[str] = [] # Permissions from API key (for API key clients)

    # Add other common attributes you might want to expose
    # Example: email: Optional[str] = None

    class Config:
        from_attributes = True # For Pydantic v2, or from_attributes = True for Pydantic v1