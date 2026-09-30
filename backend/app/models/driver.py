from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    cdl_number = Column(String, nullable=True)
    license_expiration = Column(String, nullable=True)
    medical_card_expiration = Column(String, nullable=True)
    preferred_lanes = Column(String, nullable=True)
    home_time = Column(String, nullable=True)
    no_go_states = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    status = Column(String, default="active")

    truck = relationship(
        "Truck",
        back_populates="driver",
        uselist=False,
        foreign_keys="Truck.driver_id",
        passive_deletes=True,
    )
