from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class BusinessBase(BaseModel):
    name: str
    legal_name: str | None = None
    business_type: Literal["company", "owner_operator"] = "company"
    phone: str | None = None
    email: str | None = None


class BusinessCreate(BusinessBase):
    pass


class BusinessRead(BusinessBase):
    id: int
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
