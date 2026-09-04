"""Pydantic schemas for Property."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PropertyBase(BaseModel):
    name: str = Field(..., max_length=200)
    address: str = Field(..., max_length=300)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=50)
    zip_code: str = Field(..., max_length=20)
    property_type: str = Field(..., max_length=50)
    year_built: Optional[int] = None


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    address: Optional[str] = Field(None, max_length=300)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=50)
    zip_code: Optional[str] = Field(None, max_length=20)
    property_type: Optional[str] = Field(None, max_length=50)
    year_built: Optional[int] = None


class PropertyResponse(PropertyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
