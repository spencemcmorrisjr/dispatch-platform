from pathlib import Path

root = Path("app")

files = {
    "schemas/financial_audit.py": '''from datetime import datetime

from pydantic import BaseModel


class FinancialAuditRead(BaseModel):
    id: int
    business_id: int
    load_id: int
    requester_user_id: int | None = None
    approver_user_id: int | None = None
    action: str
    field_name: str
    original_amount: str | None = None
    new_amount: str | None = None
    difference: str | None = None
    reason: str
    permission_used: str | None = None
    previous_value: str | None = None
    new_value: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
''',

    "routes/financial_audit.py": '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.financial_audit import FinancialAuditLog
from app.schemas.financial_audit import FinancialAuditRead


router = APIRouter(tags=["Financial Audit"])


@router.get(
    "/financial-audit/{load_id}",
    response_model=list[FinancialAuditRead],
    summary="View financial audit history",
)
def read_financial_audit(
    load_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(FinancialAuditLog)
        .filter(FinancialAuditLog.load_id == load_id)
        .order_by(FinancialAuditLog.created_at.desc())
        .all()
    )
''',
}

for relative_path, content in files.items():
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

main = root / "main.py"
content = main.read_text(encoding="utf-8")

route_import = "from app.routes import financial_audit\n"
if route_import not in content:
    marker = "from app.routes import rate_policy\n"
    content = content.replace(marker, marker + route_import)

router_line = "app.include_router(financial_audit.router)\n"
if router_line not in content:
    marker = "app.include_router(rate_policy.router)\n"
    content = content.replace(marker, marker + router_line)

main.write_text(content, encoding="utf-8")

print("FINANCIAL AUDIT API FILES CREATED")
