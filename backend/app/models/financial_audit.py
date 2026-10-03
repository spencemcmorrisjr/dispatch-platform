from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.database import Base


class FinancialAuditLog(Base):
    __tablename__ = "financial_audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(Integer, nullable=False, index=True)
    load_id = Column(Integer, nullable=False, index=True)

    requester_user_id = Column(Integer, nullable=True, index=True)
    approver_user_id = Column(Integer, nullable=True, index=True)

    action = Column(String(100), nullable=False)
    field_name = Column(String(100), nullable=False)

    original_amount = Column(String(50), nullable=True)
    new_amount = Column(String(50), nullable=True)
    difference = Column(String(50), nullable=True)

    reason = Column(Text, nullable=False)
    permission_used = Column(String(100), nullable=True)

    previous_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
