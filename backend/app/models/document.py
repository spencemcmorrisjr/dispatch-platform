from sqlalchemy import Column, DateTime, Integer, String, Text, func
from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=True, index=True)
    driver_id = Column(Integer, nullable=True, index=True)
    load_id = Column(Integer, nullable=True, index=True)

    document_type = Column(String(100), nullable=False)
    file_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="unpaid")
    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
