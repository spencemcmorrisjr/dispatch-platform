from typing import Literal

from pydantic import BaseModel


class MembershipBase(BaseModel):
    business_id: int
    user_id: int
    role: Literal[
        "owner_admin",
        "manager",
        "dispatcher",
        "independent_dispatcher",
        "driver",
    ] = "driver"


class MembershipCreate(MembershipBase):
    pass


class MembershipRead(MembershipBase):
    id: int
    active: bool

    class Config:
        from_attributes = True
