from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.financial_audit import FinancialAuditLog
from app.schemas.financial_audit import FinancialAuditRead
from app.services.permission_guard import require_permission


router = APIRouter(tags=["Financial Audit"])


@router.get(
    "/financial-audit/{load_id}",
    response_model=list[FinancialAuditRead],
    summary="View financial audit history",
)
def read_financial_audit(
    load_id: int,
    membership_id: int = Depends(
        require_permission("financial_audit.view")
    ),
    db: Session = Depends(get_db),
):
    return (
        db.query(FinancialAuditLog)
        .filter(FinancialAuditLog.load_id == load_id)
        .order_by(FinancialAuditLog.created_at.desc())
        .all()
    )
