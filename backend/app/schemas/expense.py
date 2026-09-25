from typing import Optional
from pydantic import BaseModel


class ExpenseBase(BaseModel):
    driver_id: Optional[int] = None
    truck_id: Optional[int] = None
    load_id: Optional[int] = None

    expense_type: str
    amount: float
    expense_date: str

    vendor: Optional[str] = None
    receipt_number: Optional[str] = None
    description: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseRead(ExpenseBase):
    id: int

    class Config:
        from_attributes = True
