from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Load(Base):
    __tablename__ = "loads"

    id = Column(Integer, primary_key=True, index=True)
    load_number = Column(String, unique=True, index=True)
    broker_name = Column(String)
    pickup_location = Column(String)
    delivery_location = Column(String)
    pickup_date = Column(String)
    delivery_date = Column(String)
    rate = Column(String)
    status = Column(String, default="available")

    driver_id = Column(Integer, ForeignKey("drivers.id"))
    truck_id = Column(Integer, ForeignKey("trucks.id"))