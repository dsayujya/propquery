"""Support ticket models — SupportTicket and SupportTicketUpdate."""

from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SupportTicket(Base):
    """An application support ticket for tracking software/system issues.

    Follows the workflow: OPEN → INVESTIGATING → RESOLVED
    """

    __tablename__ = "support_tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="open", index=True
    )

    # Optional relationships to property/unit/tenant
    property_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("properties.id", ondelete="SET NULL"), nullable=True
    )
    unit_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("units.id", ondelete="SET NULL"), nullable=True
    )
    tenant_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="SET NULL"), nullable=True
    )

    assigned_engineer: Mapped[str | None] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )
    resolved_at: Mapped[datetime | None] = mapped_column(nullable=True)
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "status IN ('open', 'investigating', 'resolved')",
            name="chk_ticket_status",
        ),
        CheckConstraint(
            "priority IN ('low', 'medium', 'high', 'critical')",
            name="chk_ticket_priority",
        ),
        CheckConstraint(
            "category IN ('reporting', 'payments', 'leases', 'maintenance', 'accounts', 'system', 'other')",
            name="chk_ticket_category",
        ),
    )

    # Relationships
    property = relationship("Property", back_populates="support_tickets")
    unit = relationship("Unit", back_populates="support_tickets")
    tenant = relationship("Tenant", back_populates="support_tickets")
    updates = relationship(
        "SupportTicketUpdate", back_populates="ticket", cascade="all, delete-orphan",
        order_by="SupportTicketUpdate.created_at",
    )

    def __repr__(self) -> str:
        return f"<SupportTicket(id={self.id}, title='{self.title}', status='{self.status}')>"


class SupportTicketUpdate(Base):
    """A historical record of an update made to a support ticket."""

    __tablename__ = "support_ticket_updates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticket_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("support_tickets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    update_type: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    old_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    new_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )

    # Relationships
    ticket = relationship("SupportTicket", back_populates="updates")

    def __repr__(self) -> str:
        return f"<SupportTicketUpdate(id={self.id}, ticket_id={self.ticket_id}, type='{self.update_type}')>"
