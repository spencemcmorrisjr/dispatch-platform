from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ExpenseType(str, Enum):
    fuel = "fuel"
    maintenance = "maintenance"
    toll = "toll"
    parking = "parking"
    lumper = "lumper"
    scale = "scale"
    permit = "permit"
    insurance = "insurance"
    registration = "registration"
    other = "other"


class ExpenseBase(BaseModel):
    expense_type: ExpenseType
    amount: float = Field(gt=0)
    expense_date: date
    vendor: Optional[str] = None
    receipt_number: Optional[str] = None
    description: Optional[str] = None
    driver_id: Optional[int] = None
    truck_id: Optional[int] = None
    load_id: Optional[int] = None

    @field_validator("expense_date")
    @classmethod
    def validate_expense_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("expense_date cannot be in the future")
        return value


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    expense_type: Optional[ExpenseType] = None
    amount: Optional[float] = Field(default=None, gt=0)
    expense_date: Optional[date] = None
    vendor: Optional[str] = None
    receipt_number: Optional[str] = None
    description: Optional[str] = None
    driver_id: Optional[int] = None
    truck_id: Optional[int] = None
    load_id: Optional[int] = None

    @field_validator("expense_date")
    @classmethod
    def validate_expense_date(cls, value: Optional[date]) -> Optional[date]:
        if value is not None and value > date.today():
            raise ValueError("expense_date cannot be in the future")
        return value


class ExpenseRead(ExpenseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
