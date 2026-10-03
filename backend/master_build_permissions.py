from pathlib import Path

root = Path("app")

files = {
    "models/role_permission.py": '''from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50), nullable=False, index=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
''',

    "models/membership_permission.py": '''from sqlalchemy import Column, ForeignKey, Integer
from app.database import Base


class MembershipPermission(Base):
    __tablename__ = "membership_permissions"

    id = Column(Integer, primary_key=True, index=True)
    membership_id = Column(
        Integer,
        ForeignKey("business_memberships.id"),
        nullable=False,
        index=True,
    )
    permission_id = Column(
        Integer,
        ForeignKey("permissions.id"),
        nullable=False,
        index=True,
    )
''',

    "schemas/permission.py": '''from pydantic import BaseModel


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
''',

    "schemas/membership.py": '''from typing import Literal

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
''',

    "routes/permission.py": '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionRead


router = APIRouter(tags=["Permissions"])


@router.post(
    "/permissions/",
    response_model=PermissionRead,
    summary="Create permission",
)
def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
):
    db_permission = Permission(
        key=permission.key,
        name=permission.name,
        description=permission.description,
    )

    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)

    return db_permission


@router.get(
    "/permissions/",
    response_model=list[PermissionRead],
    summary="View all permissions",
)
def read_permissions(db: Session = Depends(get_db)):
    return db.query(Permission).all()
''',

    "routes/membership.py": '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.membership import BusinessMembership
from app.schemas.membership import MembershipCreate, MembershipRead


router = APIRouter(tags=["Memberships"])


@router.post(
    "/memberships/",
    response_model=MembershipRead,
    summary="Create business membership",
)
def create_membership(
    membership: MembershipCreate,
    db: Session = Depends(get_db),
):
    db_membership = BusinessMembership(
        business_id=membership.business_id,
        user_id=membership.user_id,
        role=membership.role,
    )

    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)

    return db_membership


@router.get(
    "/memberships/",
    response_model=list[MembershipRead],
    summary="View all memberships",
)
def read_memberships(db: Session = Depends(get_db)):
    return db.query(BusinessMembership).all()
''',
}

# Create only the new files.
for relative_path, content in files.items():
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

# Update model registry.
models_init = root / "models" / "__init__.py"
existing = models_init.read_text(encoding="utf-8")

imports = [
    "from app.models.role_permission import RolePermission",
    "from app.models.membership_permission import MembershipPermission",
]

for line in imports:
    if line not in existing:
        existing = existing.rstrip() + "\n" + line + "\n"

for name in ["RolePermission", "MembershipPermission"]:
    if f'"{name}"' not in existing:
        existing = existing.rstrip()
        if existing.endswith("]"):
            existing = existing[:-1].rstrip()
            if not existing.endswith(","):
                existing += ","
            existing += f'\n    "{name}",\n]\n'

models_init.write_text(existing, encoding="utf-8")

# Update main.py imports and router registration.
main = root / "main.py"
content = main.read_text(encoding="utf-8")

model_import = "from app.models import role_permission as role_permission_model\nfrom app.models import membership_permission as membership_permission_model\n"
if model_import not in content:
    marker = "from app.models import business as business_model\n"
    content = content.replace(
        marker,
        marker + model_import,
    )

route_import = "from app.routes import permission\nfrom app.routes import membership\n"
if route_import not in content:
    marker = "from app.routes import business\n"
    content = content.replace(
        marker,
        marker + route_import,
    )

router_lines = "app.include_router(permission.router)\napp.include_router(membership.router)\n"
if router_lines not in content:
    marker = "app.include_router(business.router)\n"
    content = content.replace(
        marker,
        marker + router_lines,
    )

main.write_text(content, encoding="utf-8")

print("MASTER BUILD PHASE 2 FILES CREATED")
