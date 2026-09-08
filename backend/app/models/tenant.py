"""Tenant model — represents an individual who can hold a lease."""

from datetime import datetime

from sqlalchemy import Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Tenant(Base):
    """A tenant who can hold leases on units."""

    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user = relationship("User")
    leases = relationship("Lease", back_populates="tenant")
    support_tickets = relationship("SupportTicket", back_populates="tenant")

    def __repr__(self) -> str:
        return f"<Tenant(id={self.id}, name='{self.first_name} {self.last_name}')>"
