"""SQLAlchemy models package.

Import all models here so Alembic and Base.metadata can discover them.
"""

from app.models.lease import Lease
from app.models.maintenance import MaintenanceRequest
from app.models.payment import Payment
from app.models.property import Property
from app.models.support import SupportTicket, SupportTicketUpdate
from app.models.tenant import Tenant
from app.models.unit import Unit
from app.models.user import User

__all__ = [
    "Lease",
    "MaintenanceRequest",
    "Payment",
    "Property",
    "SupportTicket",
    "SupportTicketUpdate",
    "Tenant",
    "Unit",
    "User",
]
