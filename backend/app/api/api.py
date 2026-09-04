from fastapi import APIRouter, Depends
from app.api.deps import get_current_user

from .routes.properties import router as properties_router
from .routes.units import router as units_router
from .routes.tenants import router as tenants_router
from .routes.leases import router as leases_router
from .routes.payments import router as payments_router
from .routes.maintenance import router as maintenance_router
from .routes.support import router as support_router
from .routes.reports import router as reports_router
from .routes.auth import router as auth_router

api_router = APIRouter()

# Auth routes are public
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Secure all other routes
secured = [Depends(get_current_user)]

api_router.include_router(properties_router, prefix="/properties", tags=["Properties"], dependencies=secured)
api_router.include_router(units_router, prefix="/units", tags=["Units"], dependencies=secured)
api_router.include_router(tenants_router, prefix="/tenants", tags=["Tenants"], dependencies=secured)
api_router.include_router(leases_router, prefix="/leases", tags=["Leases"], dependencies=secured)
api_router.include_router(payments_router, prefix="/payments", tags=["Payments"], dependencies=secured)
api_router.include_router(maintenance_router, prefix="/maintenance", tags=["Maintenance"], dependencies=secured)
api_router.include_router(support_router, prefix="/support", tags=["Support"], dependencies=secured)
api_router.include_router(reports_router, prefix="/reports", tags=["Reports"], dependencies=secured)
