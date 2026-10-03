from typing import Literal

from pydantic import BaseModel


class RatePolicyBase(BaseModel):
    business_id: int
    rate_change_mode: Literal[
        "automatic",
        "require_approval",
        "locked",
    ] = "require_approval"

    lock_after_pickup: bool = True
    allow_driver_rate_view: bool = False
    allow_driver_rate_confirmation_view: bool = False


class RatePolicyCreate(RatePolicyBase):
    pass


class RatePolicyRead(RatePolicyBase):
    id: int

    class Config:
        from_attributes = True
