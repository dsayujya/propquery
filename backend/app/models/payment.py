"""Payment model — represents a rent payment against a lease."""

from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Payment(Base):
    """A payment made by a tenant against a lease."""

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lease_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("leases.id", ondelete="CASCADE"), nullable=False, index=True
    )
    payment_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="completed", index=True
    )
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reference_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint("amount > 0", name="chk_payment_amount"),
        CheckConstraint(
            "status IN ('completed', 'pending', 'failed', 'refunded')",
            name="chk_payment_status",
        ),
    )

    # Relationships
    lease = relationship("Lease", back_populates="payments")

    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, lease_id={self.lease_id}, amount={self.amount}, status='{self.status}')>"
