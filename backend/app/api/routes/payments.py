"""API routes for Payments."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from app.services import payment_service

router = APIRouter()

@router.get("/", response_model=List[PaymentResponse])
def read_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return payment_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(obj_in: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.create(db, obj_in=obj_in)

@router.get("/{id}", response_model=PaymentResponse)
def read_payment(id: int, db: Session = Depends(get_db)):
    return payment_service.get(db, id=id)

@router.patch("/{id}", response_model=PaymentResponse)
def update_payment(id: int, obj_in: PaymentUpdate, db: Session = Depends(get_db)):
    return payment_service.update(db, id=id, obj_in=obj_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(id: int, db: Session = Depends(get_db)):
    payment_service.remove(db, id=id)
