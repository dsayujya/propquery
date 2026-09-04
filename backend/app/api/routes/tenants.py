"""API routes for Tenants."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantResponse
from app.services import tenant_service

router = APIRouter()

@router.get("/", response_model=List[TenantResponse])
def read_tenants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return tenant_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(obj_in: TenantCreate, db: Session = Depends(get_db)):
    return tenant_service.create(db, obj_in=obj_in)

@router.get("/{id}", response_model=TenantResponse)
def read_tenant(id: int, db: Session = Depends(get_db)):
    return tenant_service.get(db, id=id)

@router.patch("/{id}", response_model=TenantResponse)
def update_tenant(id: int, obj_in: TenantUpdate, db: Session = Depends(get_db)):
    return tenant_service.update(db, id=id, obj_in=obj_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant(id: int, db: Session = Depends(get_db)):
    tenant_service.remove(db, id=id)
