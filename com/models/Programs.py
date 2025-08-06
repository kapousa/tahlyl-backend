# com/models/Programs.py

from datetime import datetime
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId


# This class handles the correct mapping of ObjectId to str in Pydantic.
# It ensures that when you retrieve an item from MongoDB, the '_id' field,
# which is an ObjectId, is correctly transformed into the 'id' string field
# on your Pydantic model.
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


class OfferDetails(BaseModel):
    """
    Pydantic model for offer details.
    Adjusted to reflect observed data variations.
    """
    type: Literal["discount", "free_trial", "bundle", "percentage_off", "info_pack"] = Field(...)
    value: Optional[str] = None
    duration: Optional[str] = None
    code: Optional[str] = None
    link: Optional[str] = None
    promo_code: Optional[str] = None

    model_config = {
        "extra": "allow"
    }


class Program(BaseModel):
    """
    Pydantic model for a Program document in MongoDB.
    Corrected to handle ObjectId mapping to a string 'id'.
    """
    # The 'id' field is mapped from the MongoDB '_id' field.
    # We use PyObjectId to ensure it is always a string.
    id: str = Field(alias='_id')
    title: str
    body: str
    created_by: str
    created_dte: datetime
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    image: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    vendor_id: str = Field(...)
    offer_details: Optional[OfferDetails] = None
    linked_health_issues: List[str] = Field(default_factory=list)

    # Use model_config to configure Pydantic's behavior.
    # 'populate_by_name': Allows Pydantic to use the alias (e.g., '_id') to populate the field.
    # 'arbitrary_types_allowed': Lets Pydantic work with custom types like ObjectId.
    # 'json_encoders': This is the key part. It tells Pydantic how to serialize
    # a specific type (ObjectId) when the model is converted to JSON,
    # ensuring it's always a string.
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "id": "60d0fe4f56f4d2217c2f1f23",
                "title": "Healthy Heart Diet Plan (7 Days)",
                "body": "A dietitian-designed meal plan...",
                "created_by": "Admin",
                "created_dte": "2025-07-22T10:00:00",
                "start_date": "2025-08-01T00:00:00",
                "end_date": "2025-12-31T23:59:59",
                "image": "https://example.com/images/heart_diet.jpg",
                "tags": ["diet", "cardiovascular", "cholesterol", "wellness"],
                "vendor_id": "vendor_xyz_123",
                "offer_details": {
                    "type": "discount",
                    "value": "20% off",
                    "code": "HEART20"
                },
                "linked_health_issues": ["cardiovascular disease"]
            }
        }
    }
