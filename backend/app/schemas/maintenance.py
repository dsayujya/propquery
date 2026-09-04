"""Pydantic schemas for MaintenanceRequest."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class MaintenanceBase(BaseModel):
    unit_id: int
    title: str = Field(..., max_length=200)
    description: str
    priority: str = Field(default="medium", max_length=20)
    status: str = Field(default="open", max_length=20)
    resolution_notes: Optional[str] = None


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(BaseModel):
    unit_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = Field(None, max_length=20)
    resolution_notes: Optional[str] = None


class MaintenanceResponse(MaintenanceBase):
    id: int
    created_date: date
    resolved_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
