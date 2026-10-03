from pydantic import BaseModel


class PermissionBase(BaseModel):
    key: str
    name: str
    description: str | None = None


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: int
    active: bool

    class Config:
        from_attributes = True
