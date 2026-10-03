from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.authorization import has_permission


def require_permission(permission_key: str):
    def permission_dependency(
        membership_id: int,
        db: Session = Depends(get_db),
    ):
        if not has_permission(
            db=db,
            membership_id=membership_id,
            permission_key=permission_key,
        ):
            raise HTTPException(
                status_code=403,
                detail=f"Permission required: {permission_key}",
            )

        return membership_id

    return permission_dependency
