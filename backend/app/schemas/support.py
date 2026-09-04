"""Pydantic schemas for SupportTicket and Updates."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SupportTicketUpdateBase(BaseModel):
    update_type: str = Field(..., max_length=50)
    content: str
    author: str = Field(..., max_length=100)
    old_status: Optional[str] = Field(None, max_length=20)
    new_status: Optional[str] = Field(None, max_length=20)


class SupportTicketUpdateCreate(SupportTicketUpdateBase):
    pass


class SupportTicketUpdateResponse(SupportTicketUpdateBase):
    id: int
    ticket_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class SupportTicketBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: str
    category: str = Field(..., max_length=50)
    priority: str = Field(default="medium", max_length=20)
    status: str = Field(default="open", max_length=20)
    property_id: Optional[int] = None
    unit_id: Optional[int] = None
    tenant_id: Optional[int] = None
    assigned_engineer: Optional[str] = Field(None, max_length=100)
    resolution_notes: Optional[str] = None


class SupportTicketCreate(SupportTicketBase):
    pass


class SupportTicketUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    priority: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = Field(None, max_length=20)
    property_id: Optional[int] = None
    unit_id: Optional[int] = None
    tenant_id: Optional[int] = None
    assigned_engineer: Optional[str] = Field(None, max_length=100)
    resolution_notes: Optional[str] = None


class SupportTicketResponse(SupportTicketBase):
    id: int
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class SupportTicketWithUpdatesResponse(SupportTicketResponse):
    updates: List[SupportTicketUpdateResponse] = []
