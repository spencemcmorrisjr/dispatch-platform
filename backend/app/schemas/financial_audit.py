from datetime import datetime

from pydantic import BaseModel


class FinancialAuditRead(BaseModel):
    id: int
    business_id: int
    load_id: int
    requester_user_id: int | None = None
    approver_user_id: int | None = None
    action: str
    field_name: str
    original_amount: str | None = None
    new_amount: str | None = None
    difference: str | None = None
    reason: str
    permission_used: str | None = None
    previous_value: str | None = None
    new_value: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
