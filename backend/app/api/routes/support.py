"""API routes for Support Tickets."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.support import (
    SupportTicketCreate,
    SupportTicketUpdateSchema,
    SupportTicketResponse,
    SupportTicketWithUpdatesResponse,
    SupportTicketUpdateCreate,
    SupportTicketUpdateResponse,
)
from app.services.support_service import support_service
from app.repositories import support_ticket_repo
from app.utils.exceptions import NotFoundException

router = APIRouter()

@router.get("/", response_model=List[SupportTicketResponse])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return support_ticket_repo.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=SupportTicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(obj_in: SupportTicketCreate, author: str = "System", db: Session = Depends(get_db)):
    return support_service.create_ticket(db, ticket_in=obj_in, author=author)

@router.get("/{id}", response_model=SupportTicketWithUpdatesResponse)
def read_ticket(id: int, db: Session = Depends(get_db)):
    ticket = support_ticket_repo.get(db, id=id)
    if not ticket:
        raise NotFoundException(detail="Support ticket not found")
    return ticket

@router.patch("/{id}", response_model=SupportTicketResponse)
def update_ticket(id: int, obj_in: SupportTicketUpdateSchema, author: str = "System", db: Session = Depends(get_db)):
    return support_service.update_ticket(db, ticket_id=id, ticket_in=obj_in, author=author)

@router.post("/{id}/updates", response_model=SupportTicketUpdateResponse)
def add_ticket_update(id: int, obj_in: SupportTicketUpdateCreate, db: Session = Depends(get_db)):
    return support_service.add_update(db, ticket_id=id, update_in=obj_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(id: int, db: Session = Depends(get_db)):
    ticket = support_ticket_repo.get(db, id=id)
    if not ticket:
        raise NotFoundException(detail="Support ticket not found")
    support_ticket_repo.remove(db, id=id)
