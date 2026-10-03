from sqlalchemy.orm import Session

from app.models.membership import BusinessMembership
from app.models.permission import Permission
from app.models.membership_permission import MembershipPermission


def has_permission(
    db: Session,
    membership_id: int,
    permission_key: str,
) -> bool:
    permission = (
        db.query(Permission)
        .filter(Permission.key == permission_key)
        .first()
    )

    if permission is None:
        return False

    assignment = (
        db.query(MembershipPermission)
        .filter(
            MembershipPermission.membership_id == membership_id,
            MembershipPermission.permission_id == permission.id,
        )
        .first()
    )

    return assignment is not None


def get_membership(
    db: Session,
    membership_id: int,
):
    return (
        db.query(BusinessMembership)
        .filter(BusinessMembership.id == membership_id)
        .first()
    )
