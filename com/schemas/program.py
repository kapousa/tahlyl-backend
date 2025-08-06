# src/schemas.py (or a new file like src/schemas/programs.py)

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Assuming your AnalysisResult, AnalysisDetailedResultItem are already defined here.
# ... (your existing AnalysisResult and AnalysisDetailedResultItem definitions) ...

# --- Original Pydantic Models for Programs/Offers (as provided by you) ---

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

# --- NEW: Pydantic Models for Detailed Program Response ---

# This flexible OfferDetails model is specifically for the detailed program response.
# It's designed to be highly tolerant of varied data, allowing 'type' to be any string
# and other fields to be optional and of 'Any' type.
class OfferDetailsFlexible(BaseModel):
    type: str
    value: Optional[Any] = None
    code: Optional[str] = None
    link: Optional[str] = None
    promo_code: Optional[str] = None

    class Config:
        extra = "allow" # Allows for any other fields to be included

# This model is for individual benefits within a program's detailed view.
class ProgramBenefitFlexible(BaseModel):
    id: Optional[str] = None
    text: Optional[str] = None
    icon: Optional[str] = None

    class Config:
        extra = "allow" # Allows for any other fields to be included

# This model represents a module within a program's detailed structure.
class ProgramModule(BaseModel):
    id: str
    title: str
    description: str

    class Config:
        extra = "allow" # Allows for any other fields to be included

# ⭐ ProgramDetailResponseFlexible ⭐
# This is the full detail response model for a program page,
# designed to be used when fetching a single program with all its details.
class ProgramDetailResponseFlexible(BaseModel):
    # Map MongoDB's '_id' field to the 'id' attribute in the Pydantic model.
    id: str = Field(alias='_id')
    title: str
    # These fields are now Optional as they might be missing in some documents
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    banner_image_url: Optional[str] = None
    validity_date: Optional[str] = None # Consider changing to datetime if it's a date string
    price: Optional[str] = None

    # Link to the flexible OfferDetails model for program-specific offers.
    offer_details: Optional[OfferDetailsFlexible] = None

    # List of flexible ProgramBenefit models associated with this program.
    benefits: Optional[List[ProgramBenefitFlexible]] = None
    # List of ProgramModule models that compose this program.
    modules: Optional[List[ProgramModule]] = None

    class Config:
        # This setting is crucial for Pydantic to recognize and map '_id' from MongoDB
        # to the 'id' field in this model.
        populate_by_name = True
        # Allow any extra fields that might exist in the database document but are
        # not explicitly defined in this Pydantic model.
        extra = "allow"
