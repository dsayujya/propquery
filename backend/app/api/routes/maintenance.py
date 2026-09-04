"""API routes for MaintenanceRequests."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.maintenance import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse
from app.services import maintenance_service

router = APIRouter()

@router.get("/", response_model=List[MaintenanceResponse])
def read_maintenance_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return maintenance_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=MaintenanceResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance_request(obj_in: MaintenanceCreate, db: Session = Depends(get_db)):
    return maintenance_service.create(db, obj_in=obj_in)

@router.get("/{id}", response_model=MaintenanceResponse)
def read_maintenance_request(id: int, db: Session = Depends(get_db)):
    return maintenance_service.get(db, id=id)

@router.patch("/{id}", response_model=MaintenanceResponse)
def update_maintenance_request(id: int, obj_in: MaintenanceUpdate, db: Session = Depends(get_db)):
    return maintenance_service.update(db, id=id, obj_in=obj_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_maintenance_request(id: int, db: Session = Depends(get_db)):
    maintenance_service.remove(db, id=id)
