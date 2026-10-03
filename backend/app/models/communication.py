from sqlalchemy import Column, DateTime, Integer, String, Text, func
from app.database import Base


class CommunicationTimeline(Base):
    __tablename__ = "communication_timeline"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=True, index=True)
    load_id = Column(Integer, nullable=True, index=True)
    driver_id = Column(Integer, nullable=True, index=True)

    communication_type = Column(String(50), nullable=False)
    direction = Column(String(20), nullable=True)
    subject = Column(String(255), nullable=True)
    message = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
