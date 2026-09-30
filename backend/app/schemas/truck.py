from pydantic import BaseModel


class TruckBase(BaseModel):
    unit_number: str
    vin: str | None = None
    year: str | None = None
    make: str | None = None
    model: str | None = None
    license_plate: str | None = None
    dot_inspection_expiration: str | None = None
    insurance_expiration: str | None = None
    status: str = "active"
    driver_id: int | None = None


class TruckCreate(TruckBase):
    pass


class TruckRead(TruckBase):
    id: int
    driver_name: str | None = None
    driver_company_name: str | None = None

    class Config:
        from_attributes = True
