from pydantic import BaseModel


class MembershipPermissionCreate(BaseModel):
    membership_id: int
    permission_id: int


class MembershipPermissionRead(BaseModel):
    id: int
    membership_id: int
    permission_id: int

    class Config:
        from_attributes = True
