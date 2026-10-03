from fastapi import APIRouter, Depends
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
