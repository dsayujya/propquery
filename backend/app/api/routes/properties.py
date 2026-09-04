"""API routes for Properties."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyResponse
from app.services import property_service

router = APIRouter()

@router.get("/", response_model=List[PropertyResponse])
def read_properties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return property_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(obj_in: PropertyCreate, db: Session = Depends(get_db)):
    return property_service.create(db, obj_in=obj_in)

@router.get("/{id}", response_model=PropertyResponse)
def read_property(id: int, db: Session = Depends(get_db)):
    return property_service.get(db, id=id)

@router.patch("/{id}", response_model=PropertyResponse)
def update_property(id: int, obj_in: PropertyUpdate, db: Session = Depends(get_db)):
    return property_service.update(db, id=id, obj_in=obj_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(id: int, db: Session = Depends(get_db)):
    property_service.remove(db, id=id)
