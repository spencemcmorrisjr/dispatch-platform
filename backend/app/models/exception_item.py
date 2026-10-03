from sqlalchemy import Column, DateTime, Integer, String, Text, func
from app.database import Base


class ExceptionItem(Base):
    __tablename__ = "exception_items"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=True, index=True)
    load_id = Column(Integer, nullable=True, index=True)
    driver_id = Column(Integer, nullable=True, index=True)

    exception_type = Column(String(100), nullable=False)
    severity = Column(String(30), nullable=False, default="warning")
    status = Column(String(30), nullable=False, default="open")
    description = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
