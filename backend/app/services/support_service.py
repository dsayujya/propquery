"""Support ticket service with business logic."""

from sqlalchemy.orm import Session

from app.models.support import SupportTicket, SupportTicketUpdate
from app.repositories import support_ticket_repo, support_ticket_update_repo
from app.schemas.support import SupportTicketCreate, SupportTicketUpdateSchema, SupportTicketUpdateCreate
from app.utils.exceptions import NotFoundException


class SupportTicketService:
    @staticmethod
    def create_ticket(db: Session, ticket_in: SupportTicketCreate, author: str = "System") -> SupportTicket:
        """Create a new ticket and its initial update record."""
        ticket = support_ticket_repo.create(db, obj_in=ticket_in)

        # Create initial update record
        update_in = SupportTicketUpdateCreate(
            update_type="created",
            content=f"Ticket created with status '{ticket.status}'",
            author=author,
            new_status=ticket.status
        )
        
        # Link the update to the ticket
        update_obj = support_ticket_update_repo.model(**update_in.model_dump(), ticket_id=ticket.id)
        db.add(update_obj)
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def update_ticket(
        db: Session, ticket_id: int, ticket_in: SupportTicketUpdateSchema, author: str = "System"
    ) -> SupportTicket:
        """Update a ticket and create an audit log if status changes."""
        ticket = support_ticket_repo.get(db, id=ticket_id)
        if not ticket:
            raise NotFoundException(detail="Support ticket not found")

        old_status = ticket.status
        old_resolution_notes = ticket.resolution_notes
        new_status = ticket_in.status if ticket_in.status else old_status

        updated_ticket = support_ticket_repo.update(db, db_obj=ticket, obj_in=ticket_in)

        # If status changed, create an update record
        if old_status != new_status:
            update_in = SupportTicketUpdateCreate(
                update_type="status_change",
                content=f"Status changed from {old_status} to {new_status}",
                author=author,
                old_status=old_status,
                new_status=new_status
            )
            update_obj = support_ticket_update_repo.model(**update_in.model_dump(), ticket_id=updated_ticket.id)
            db.add(update_obj)
            db.commit()

        # If resolution notes were added, maybe log that too
        if ticket_in.resolution_notes and ticket_in.resolution_notes != old_resolution_notes:
            note_in = SupportTicketUpdateCreate(
                update_type="resolution_note_added",
                content="Resolution notes added/updated.",
                author=author
            )
            note_obj = support_ticket_update_repo.model(**note_in.model_dump(), ticket_id=updated_ticket.id)
            db.add(note_obj)
            db.commit()
            
        db.refresh(updated_ticket)
        return updated_ticket

    @staticmethod
    def add_update(
        db: Session, ticket_id: int, update_in: SupportTicketUpdateCreate
    ) -> SupportTicketUpdate:
        """Add a manual update/comment to a ticket."""
        ticket = support_ticket_repo.get(db, id=ticket_id)
        if not ticket:
            raise NotFoundException(detail="Support ticket not found")

        update_obj = support_ticket_update_repo.model(**update_in.model_dump(), ticket_id=ticket.id)
        db.add(update_obj)
        db.commit()
        db.refresh(update_obj)
        return update_obj

support_service = SupportTicketService()
