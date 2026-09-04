"""Pydantic schemas for Lease."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class LeaseBase(BaseModel):
    unit_id: int
    tenant_id: int
    start_date: date
    end_date: date
    monthly_rent: float = Field(..., gt=0)
    security_deposit: float = Field(default=0, ge=0)
    status: str = Field(default="active", max_length=20)


class LeaseCreate(LeaseBase):
    pass


class LeaseUpdate(BaseModel):
    unit_id: Optional[int] = None
    tenant_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    monthly_rent: Optional[float] = Field(None, gt=0)
    security_deposit: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, max_length=20)


class LeaseResponse(LeaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
