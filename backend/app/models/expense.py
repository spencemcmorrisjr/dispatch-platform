from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    truck_id = Column(Integer, ForeignKey("trucks.id"), nullable=True)
    load_id = Column(Integer, ForeignKey("loads.id"), nullable=True)

    expense_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    expense_date = Column(String, nullable=False)

    vendor = Column(String, nullable=True)
    receipt_number = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
