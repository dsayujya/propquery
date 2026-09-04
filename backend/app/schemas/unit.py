"""Pydantic schemas for Unit."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, condecimal


class UnitBase(BaseModel):
    property_id: int
    unit_number: str = Field(..., max_length=20)
    bedrooms: int = Field(default=1, ge=0)
    bathrooms: int = Field(default=1, ge=0)
    square_feet: Optional[float] = None
    market_rent: float = Field(..., gt=0)
    status: str = Field(default="vacant", max_length=20)


class UnitCreate(UnitBase):
    pass


class UnitUpdate(BaseModel):
    property_id: Optional[int] = None
    unit_number: Optional[str] = Field(None, max_length=20)
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[int] = Field(None, ge=0)
    square_feet: Optional[float] = None
    market_rent: Optional[float] = Field(None, gt=0)
    status: Optional[str] = Field(None, max_length=20)


class UnitResponse(UnitBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
