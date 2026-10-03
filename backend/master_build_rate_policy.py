from pathlib import Path

root = Path("app")

files = {
    "models/rate_policy.py": '''from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.database import Base


class RatePolicy(Base):
    __tablename__ = "rate_policies"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    rate_change_mode = Column(
        String(30),
        nullable=False,
        default="require_approval",
    )

    lock_after_pickup = Column(Boolean, nullable=False, default=True)
    allow_driver_rate_view = Column(Boolean, nullable=False, default=False)
    allow_driver_rate_confirmation_view = Column(
        Boolean,
        nullable=False,
        default=False,
    )
''',

    "schemas/rate_policy.py": '''from typing import Literal

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
''',

    "routes/rate_policy.py": '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.rate_policy import RatePolicy
from app.schemas.rate_policy import RatePolicyCreate, RatePolicyRead


router = APIRouter(tags=["Rate Policies"])


@router.post(
    "/rate-policies/",
    response_model=RatePolicyRead,
    summary="Create rate policy",
)
def create_rate_policy(
    policy: RatePolicyCreate,
    db: Session = Depends(get_db),
):
    db_policy = RatePolicy(
        business_id=policy.business_id,
        rate_change_mode=policy.rate_change_mode,
        lock_after_pickup=policy.lock_after_pickup,
        allow_driver_rate_view=policy.allow_driver_rate_view,
        allow_driver_rate_confirmation_view=(
            policy.allow_driver_rate_confirmation_view
        ),
    )

    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)

    return db_policy


@router.get(
    "/rate-policies/{business_id}",
    response_model=RatePolicyRead,
    summary="View business rate policy",
)
def read_rate_policy(
    business_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(RatePolicy)
        .filter(RatePolicy.business_id == business_id)
        .first()
    )
''',
}

for relative_path, content in files.items():
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

models_init = root / "models" / "__init__.py"
existing = models_init.read_text(encoding="utf-8")

import_line = "from app.models.rate_policy import RatePolicy"
if import_line not in existing:
    existing = existing.rstrip() + "\n" + import_line + "\n"

if '"RatePolicy"' not in existing:
    existing = existing.rstrip()
    if existing.endswith("]"):
        existing = existing[:-1].rstrip()
        if not existing.endswith(","):
            existing += ","
        existing += '\n    "RatePolicy",\n]\n'

models_init.write_text(existing, encoding="utf-8")

main = root / "main.py"
content = main.read_text(encoding="utf-8")

model_import = "from app.models import rate_policy as rate_policy_model\n"
if model_import not in content:
    marker = "from app.models import business as business_model\n"
    content = content.replace(marker, marker + model_import)

route_import = "from app.routes import rate_policy\n"
if route_import not in content:
    marker = "from app.routes import business\n"
    content = content.replace(marker, marker + route_import)

router_line = "app.include_router(rate_policy.router)\n"
if router_line not in content:
    marker = "app.include_router(business.router)\n"
    content = content.replace(marker, marker + router_line)

main.write_text(content, encoding="utf-8")

print("MASTER BUILD PHASE 3 FILES CREATED")
