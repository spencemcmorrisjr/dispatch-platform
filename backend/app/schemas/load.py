from pydantic import BaseModel


class LoadBase(BaseModel):
    load_number: str
    broker_name: str
    pickup_location: str
    delivery_location: str
    pickup_date: str
    delivery_date: str
    rate: str
    status: str = "available"
    driver_id: int | None = None
    truck_id: int | None = None


class LoadCreate(LoadBase):
    pass


class LoadRead(LoadBase):
    id: int

    class Config:
        from_attributes = True