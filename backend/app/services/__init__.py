"""Export all services."""

from app.repositories import (
    property_repo,
    unit_repo,
    tenant_repo,
    lease_repo,
    payment_repo,
    maintenance_repo,
)
from .base import ServiceBase
from .support_service import support_service

property_service = ServiceBase(property_repo, "Property")
unit_service = ServiceBase(unit_repo, "Unit")
tenant_service = ServiceBase(tenant_repo, "Tenant")
lease_service = ServiceBase(lease_repo, "Lease")
payment_service = ServiceBase(payment_repo, "Payment")
maintenance_service = ServiceBase(maintenance_repo, "MaintenanceRequest")

__all__ = [
    "property_service",
    "unit_service",
    "tenant_service",
    "lease_service",
    "payment_service",
    "maintenance_service",
    "support_service",
]
