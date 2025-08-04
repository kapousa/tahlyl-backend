# com/models/Programs.py

from datetime import datetime
from typing import List, Optional, Literal, Dict, Any, Annotated  # Import Annotated

from pydantic import BaseModel, Field, BeforeValidator  # Ensure BeforeValidator is imported
from bson import ObjectId


# No longer define PyObjectId as a separate variable using BeforeValidator.
# We will use Annotated directly in the field definition.

class OfferDetails(BaseModel):
    """
    Pydantic model for offer details.
    Adjusted to reflect observed data variations.
    """
    # Broaden the Literal to include all types found in your data
    type: Literal["discount", "free_trial", "bundle", "percentage_off", "info_pack"] = Field(...)

    # Make value, duration, code, link, promo_code optional,
    # as not all offer types will have all these fields.
    value: Optional[str] = None
    duration: Optional[str] = None
    code: Optional[str] = None
    link: Optional[str] = None
    promo_code: Optional[str] = None

    # Allow extra fields for flexibility if your MongoDB data might have other arbitrary fields
    model_config = {
        "extra": "allow"
    }


class Program(BaseModel):
    """
    Pydantic model for a Program document in MongoDB.
    Corrected to match MongoDB data types and structure.
    """
    # Correct way to handle ObjectId mapping to a string 'id' using Annotated
    # This tells Pydantic to apply the 'BeforeValidator(str)' to the '_id' field
    # before validating it as a 'str'.
    id: Optional[Annotated[str, BeforeValidator(str)]] = Field(alias="_id", default=None)

    title: str = Field(...)
    body: str = Field(...)
    created_by: str = Field(...)
    created_dte: datetime = Field(...)
    start_date: datetime = Field(...)

    # Make end_date optional as some documents might have it as None
    end_date: Optional[datetime] = None

    image: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    vendor_id: str = Field(...)

    # Use the corrected OfferDetails model
    offer_details: Optional[OfferDetails] = None

    linked_health_issues: List[str] = Field(default_factory=list)

    model_config = {
        "populate_by_name": True,  # Allow populating fields by alias (e.g., '_id' from MongoDB)
        "arbitrary_types_allowed": True,
        # Still good to keep if you have other non-standard types Pydantic might complain about
        "json_schema_extra": {
            "example": {
                "title": "Healthy Heart Diet Plan (7 Days)",
                "body": "A dietitian-designed meal plan...",
                "created_by": "Admin",
                "created_dte": "2025-07-22T10:00:00",
                "start_date": "2025-08-01T00:00:00",
                "end_date": "2025-12-31T23:59:59",
                "image": "https://example.com/images/heart_diet.jpg",
                "tags": ["diet", "cardiovascular", "cholesterol", "wellness"],
                "vendor_id": "nutritionCo101",
                "offer_details": {
                    "type": "discount",
                    "value": "20%",
                    "code": "TAHLYLHEALTHY20"
                },
                "linked_health_issues": ["high cholesterol"]
            }
        }
    }