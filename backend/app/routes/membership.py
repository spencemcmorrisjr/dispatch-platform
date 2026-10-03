from fastapi import APIRouter, Depends
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
