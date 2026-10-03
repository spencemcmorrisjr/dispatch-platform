from sqlalchemy import Column, ForeignKey, Integer
from app.database import Base


class MembershipPermission(Base):
    __tablename__ = "membership_permissions"

    id = Column(Integer, primary_key=True, index=True)
    membership_id = Column(
        Integer,
        ForeignKey("business_memberships.id"),
        nullable=False,
        index=True,
    )
    permission_id = Column(
        Integer,
        ForeignKey("permissions.id"),
        nullable=False,
        index=True,
    )
