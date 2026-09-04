"""Pydantic schemas for Payment."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class PaymentBase(BaseModel):
    lease_id: int
    payment_date: date
    amount: float = Field(..., gt=0)
    status: str = Field(default="completed", max_length=20)
    payment_method: Optional[str] = Field(None, max_length=50)
    reference_number: Optional[str] = Field(None, max_length=100)


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    lease_id: Optional[int] = None
    payment_date: Optional[date] = None
    amount: Optional[float] = Field(None, gt=0)
    status: Optional[str] = Field(None, max_length=20)
    payment_method: Optional[str] = Field(None, max_length=50)
    reference_number: Optional[str] = Field(None, max_length=100)


class PaymentResponse(PaymentBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
