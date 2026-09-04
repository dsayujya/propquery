"""API routes for Units."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.unit import UnitCreate, UnitUpdate, UnitResponse
from app.services import unit_service

router = APIRouter()

@router.get("/", response_model=List[UnitResponse])
def read_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return unit_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=UnitResponse, status_code=status.HTTP_201_CREATED)
def create_unit(obj_in: UnitCreate, db: Session = Depends(get_db)):
    return unit_service.create(db, obj_in=obj_in)

@router.get("/{id}", response_model=UnitResponse)
def read_unit(id: int, db: Session = Depends(get_db)):
    return unit_service.get(db, id=id)

@router.patch("/{id}", response_model=UnitResponse)
def update_unit(id: int, obj_in: UnitUpdate, db: Session = Depends(get_db)):
    return unit_service.update(db, id=id, obj_in=obj_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unit(id: int, db: Session = Depends(get_db)):
    unit_service.remove(db, id=id)
