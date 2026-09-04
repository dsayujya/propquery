"""Unit model — represents a rentable unit within a property."""

from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Unit(Base):
    """A rentable unit (apartment, suite, etc.) within a property."""

    __tablename__ = "units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    property_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False, index=True
    )
    unit_number: Mapped[str] = mapped_column(String(20), nullable=False)
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    bathrooms: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    square_feet: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    market_rent: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="vacant", index=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint("status IN ('occupied', 'vacant')", name="chk_unit_status"),
        CheckConstraint("market_rent > 0", name="chk_unit_market_rent"),
        CheckConstraint("bedrooms >= 0", name="chk_unit_bedrooms"),
        CheckConstraint("bathrooms >= 0", name="chk_unit_bathrooms"),
    )

    # Relationships
    property = relationship("Property", back_populates="units")
    leases = relationship("Lease", back_populates="unit", cascade="all, delete-orphan")
    maintenance_requests = relationship(
        "MaintenanceRequest", back_populates="unit", cascade="all, delete-orphan"
    )
    support_tickets = relationship("SupportTicket", back_populates="unit")

    def __repr__(self) -> str:
        return f"<Unit(id={self.id}, unit_number='{self.unit_number}', status='{self.status}')>"
