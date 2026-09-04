"""Repositories for all entities."""

from app.models.property import Property
from app.models.unit import Unit
from app.models.tenant import Tenant
from app.models.lease import Lease
from app.models.payment import Payment
from app.models.maintenance import MaintenanceRequest
from app.models.support import SupportTicket, SupportTicketUpdate

from app.schemas.property import PropertyCreate, PropertyUpdate
from app.schemas.unit import UnitCreate, UnitUpdate
from app.schemas.tenant import TenantCreate, TenantUpdate
from app.schemas.lease import LeaseCreate, LeaseUpdate
from app.schemas.payment import PaymentCreate, PaymentUpdate
from app.schemas.maintenance import MaintenanceCreate, MaintenanceUpdate
from app.schemas.support import SupportTicketCreate, SupportTicketUpdateSchema, SupportTicketUpdateCreate, SupportTicketUpdateBase

from .base import CRUDBase

class CRUDProperty(CRUDBase[Property, PropertyCreate, PropertyUpdate]):
    pass

class CRUDUnit(CRUDBase[Unit, UnitCreate, UnitUpdate]):
    pass

class CRUDTenant(CRUDBase[Tenant, TenantCreate, TenantUpdate]):
    pass

class CRUDLease(CRUDBase[Lease, LeaseCreate, LeaseUpdate]):
    pass

class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    pass

class CRUDMaintenance(CRUDBase[MaintenanceRequest, MaintenanceCreate, MaintenanceUpdate]):
    pass

class CRUDSupportTicket(CRUDBase[SupportTicket, SupportTicketCreate, SupportTicketUpdateSchema]):
    pass

class CRUDSupportTicketUpdate(CRUDBase[SupportTicketUpdate, SupportTicketUpdateCreate, SupportTicketUpdateBase]):
    pass


property_repo = CRUDProperty(Property)
unit_repo = CRUDUnit(Unit)
tenant_repo = CRUDTenant(Tenant)
lease_repo = CRUDLease(Lease)
payment_repo = CRUDPayment(Payment)
maintenance_repo = CRUDMaintenance(MaintenanceRequest)
support_ticket_repo = CRUDSupportTicket(SupportTicket)
support_ticket_update_repo = CRUDSupportTicketUpdate(SupportTicketUpdate)
