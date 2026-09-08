"""Pydantic schemas for Public Listings."""

from typing import List, Optional
from pydantic import BaseModel

class UnitListing(BaseModel):
    id: int
    unit_number: str
    bedrooms: int
    bathrooms: int
    square_feet: Optional[float] = None
    market_rent: float
    
    model_config = {"from_attributes": True}

class PropertyListing(BaseModel):
    id: int
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    property_type: str
    image_url: Optional[str] = None
    units: List[UnitListing]
    
    model_config = {"from_attributes": True}
