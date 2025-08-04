# src/schemas.py (or a new file like src/schemas/programs.py)

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Assuming your AnalysisResult, AnalysisDetailedResultItem are already defined here.
# ... (your existing AnalysisResult and AnalysisDetailedResultItem definitions) ...

# --- NEW: Pydantic Models for Programs/Offers ---

class OfferDetails(BaseModel):
    type: str  # e.g., "discount", "free_trial", "percentage_off", "info_pack"
    value: Optional[str] = None
    duration: Optional[str] = None
    code: Optional[str] = None
    link: Optional[str] = None
    promo_code: Optional[str] = None # Some offers might use 'code', others 'promo_code'

class ProgramOffer(BaseModel):
    # _id will be ObjectId, so it's handled by Pydantic's ObjectId field (requires pydantic-extra-types)
    # For simplicity in API response, we'll return _id as str
    id: str = Field(..., alias="_id") # Map _id from MongoDB to 'id' for Pydantic
    title: str
    body: str
    created_by: Optional[str] = None
    created_dte: Optional[datetime] = None # Will be datetime object from MongoDB
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    image: Optional[str] = None
    tags: List[str] = []
    vendor_id: str
    offer_details: OfferDetails
    linked_health_issues: List[str] = []

    class Config:
        arbitrary_types_allowed = True # Allow ObjectId type if you use it directly
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None, # Encode datetime to ISO string
            # ObjectId: str # If you explicitly return ObjectId objects, define encoder
        }
        # Use from_attributes = True for Pydantic V2 or orm_mode = True for Pydantic V1
        # if you fetch directly from SQLAlchemy models and want to convert.
        # This is for MongoDB, so from_attributes might not be directly applicable here.

# --- End NEW Models ---