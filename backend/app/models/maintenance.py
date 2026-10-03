from sqlalchemy import Column, Date, Integer, String, Text
from app.database import Base


class MaintenanceItem(Base):
    __tablename__ = "maintenance_items"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=True, index=True)
    truck_id = Column(Integer, nullable=True, index=True)

    maintenance_type = Column(String(100), nullable=False)
    due_date = Column(Date, nullable=True)
    mileage_due = Column(Integer, nullable=True)
    status = Column(String(30), nullable=False, default="scheduled")
    notes = Column(Text, nullable=True)
