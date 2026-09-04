"""API routes for Reports."""

from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.reports import report_repository
from app.schemas.reports import (
    PropertyOccupancyReport,
    RentCollectionReport,
    TenantPaymentHistory,
    OutstandingPaymentReport,
    MaintenancePerformanceReport,
    PropertyFinancialSummary,
    MonthlyRevenueReport
)

router = APIRouter()

@router.get("/occupancy", response_model=List[PropertyOccupancyReport])
def get_occupancy_report(db: Session = Depends(get_db)):
    return report_repository.get_property_occupancy(db)

@router.get("/rent-collection", response_model=List[RentCollectionReport])
def get_rent_collection_report(db: Session = Depends(get_db)):
    return report_repository.get_rent_collection(db)

@router.get("/tenant-payments", response_model=List[TenantPaymentHistory])
def get_tenant_payment_history(tenant_id: Optional[int] = None, db: Session = Depends(get_db)):
    return report_repository.get_tenant_payment_history(db, tenant_id)

@router.get("/outstanding-payments", response_model=List[OutstandingPaymentReport])
def get_outstanding_payments_report(db: Session = Depends(get_db)):
    return report_repository.get_outstanding_payments(db)

@router.get("/maintenance-performance", response_model=List[MaintenancePerformanceReport])
def get_maintenance_performance_report(db: Session = Depends(get_db)):
    return report_repository.get_maintenance_performance(db)

@router.get("/financial-summary", response_model=List[PropertyFinancialSummary])
def get_financial_summary_report(db: Session = Depends(get_db)):
    return report_repository.get_property_financial_summary(db)

@router.get("/monthly-revenue", response_model=List[MonthlyRevenueReport])
def get_monthly_revenue_report(db: Session = Depends(get_db)):
    return report_repository.get_monthly_revenue(db)
