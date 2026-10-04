from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionRead
from app.services.permission_guard import require_permission


router = APIRouter(tags=["Permissions"])


@router.post(
    "/permissions/",
    response_model=PermissionRead,
    summary="Create permission",
)
def create_permission(
    permission: PermissionCreate,
    membership_id: int = Depends(
        require_permission("permission.create")
    ),
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
def read_permissions(
    membership_id: int = Depends(
        require_permission("permission.view")
    ),
    db: Session = Depends(get_db),
):
    return db.query(Permission).all()
