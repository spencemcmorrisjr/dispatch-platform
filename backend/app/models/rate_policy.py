from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.database import Base


class RatePolicy(Base):
    __tablename__ = "rate_policies"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    rate_change_mode = Column(
        String(30),
        nullable=False,
        default="require_approval",
    )

    lock_after_pickup = Column(Boolean, nullable=False, default=True)
    allow_driver_rate_view = Column(Boolean, nullable=False, default=False)
    allow_driver_rate_confirmation_view = Column(
        Boolean,
        nullable=False,
        default=False,
    )
