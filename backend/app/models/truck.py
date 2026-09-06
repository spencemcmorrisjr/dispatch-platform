from sqlalchemy import Column, Integer, String
from app.database import Base


class Truck(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, index=True)

    unit_number = Column(String, nullable=False)
    vin = Column(String, nullable=True)

    year = Column(String, nullable=True)
    make = Column(String, nullable=True)
    model = Column(String, nullable=True)

    license_plate = Column(String, nullable=True)

    dot_inspection_expiration = Column(String, nullable=True)
    insurance_expiration = Column(String, nullable=True)

    status = Column(String, default="active")

    driver_id = Column(Integer, nullable=True)
