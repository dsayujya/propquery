"""Pydantic schemas for SQL Reports."""

from typing import Optional, List
from datetime import date
from pydantic import BaseModel


class PropertyOccupancyReport(BaseModel):
    property_name: str
    total_units: int
    occupied_units: int
    vacant_units: int
    occupancy_percentage: float


class RentCollectionReport(BaseModel):
    property_name: str
    expected_rent: float
    collected_rent: float
    outstanding_amount: float
    collection_percentage: float


class TenantPaymentHistory(BaseModel):
    tenant_name: str
    unit_number: str
    property_name: str
    payment_date: date
    amount: float
    status: str


class OutstandingPaymentReport(BaseModel):
    tenant_name: str
    property_name: str
    unit_number: str
    monthly_rent: float
    total_paid: float
    outstanding_balance: float


class MaintenancePerformanceReport(BaseModel):
    property_name: str
    total_requests: int
    open_requests: int
    resolved_requests: int
    avg_resolution_days: Optional[float]


class PropertyFinancialSummary(BaseModel):
    property_name: str
    total_revenue: float
    total_units: int
    avg_rent_per_unit: float


class MonthlyRevenueReport(BaseModel):
    revenue_month: str  # YYYY-MM
    total_revenue: float
    payment_count: int
