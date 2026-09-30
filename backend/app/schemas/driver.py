from pydantic import BaseModel


class DriverBase(BaseModel):
    name: str
    phone: str
    email: str | None = None
    cdl_number: str | None = None
    license_expiration: str | None = None
    medical_card_expiration: str | None = None
    preferred_lanes: str | None = None
    home_time: str | None = None
    no_go_states: str | None = None
    company_name: str | None = None
    status: str | None = "active"


class DriverCreate(DriverBase):
    pass


class DriverRead(DriverBase):
    id: int
    truck_id: int | None = None
    truck_unit_number: str | None = None

    class Config:
        from_attributes = True
