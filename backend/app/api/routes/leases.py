"""API routes for Leases."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.lease import LeaseCreate, LeaseUpdate, LeaseResponse
from app.services import lease_service

router = APIRouter()

@router.get("/", response_model=List[LeaseResponse])
def read_leases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return lease_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=LeaseResponse, status_code=status.HTTP_201_CREATED)
def create_lease(obj_in: LeaseCreate, db: Session = Depends(get_db)):
    return lease_service.create(db, obj_in=obj_in)

@router.get("/{id}", response_model=LeaseResponse)
def read_lease(id: int, db: Session = Depends(get_db)):
    return lease_service.get(db, id=id)

@router.patch("/{id}", response_model=LeaseResponse)
def update_lease(id: int, obj_in: LeaseUpdate, db: Session = Depends(get_db)):
    return lease_service.update(db, id=id, obj_in=obj_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lease(id: int, db: Session = Depends(get_db)):
    lease_service.remove(db, id=id)
