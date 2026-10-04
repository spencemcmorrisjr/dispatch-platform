from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.membership_permission import MembershipPermission
from app.schemas.membership_permission import (
    MembershipPermissionCreate,
    MembershipPermissionRead,
)


router = APIRouter(tags=["Membership Permissions"])


@router.post(
    "/membership-permissions/",
    response_model=MembershipPermissionRead,
    summary="Assign permission to membership",
)
def create_membership_permission(
    assignment: MembershipPermissionCreate,
    db: Session = Depends(get_db),
):
    db_assignment = MembershipPermission(
        membership_id=assignment.membership_id,
        permission_id=assignment.permission_id,
    )

    db.add(db_assignment)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Permission is already assigned to this membership.",
        )

    db.refresh(db_assignment)

    return db_assignment


@router.get(
    "/membership-permissions/",
    response_model=list[MembershipPermissionRead],
    summary="View membership permissions",
)
def read_membership_permissions(
    db: Session = Depends(get_db),
):
    return db.query(MembershipPermission).all()
