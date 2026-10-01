from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from app.database import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)
    legal_name = Column(String(200), nullable=True)

    business_type = Column(String(30), nullable=False, default="company")

    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)

    active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
