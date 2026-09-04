"""Lease model — represents a rental agreement between a tenant and a unit."""

from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Lease(Base):
    """A lease agreement linking a tenant to a unit for a specific period."""

    __tablename__ = "leases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    unit_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("units.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tenant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    monthly_rent: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    security_deposit: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="active", index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint("end_date > start_date", name="chk_lease_dates"),
        CheckConstraint("monthly_rent > 0", name="chk_lease_rent"),
        CheckConstraint("security_deposit >= 0", name="chk_lease_deposit"),
        CheckConstraint(
            "status IN ('active', 'expired', 'terminated')",
            name="chk_lease_status",
        ),
    )

    # Relationships
    unit = relationship("Unit", back_populates="leases")
    tenant = relationship("Tenant", back_populates="leases")
    payments = relationship("Payment", back_populates="lease", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Lease(id={self.id}, unit_id={self.unit_id}, tenant_id={self.tenant_id}, status='{self.status}')>"
