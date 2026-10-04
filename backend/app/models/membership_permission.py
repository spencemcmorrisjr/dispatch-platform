from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from app.database import Base


class MembershipPermission(Base):
    __tablename__ = "membership_permissions"

    __table_args__ = (
        UniqueConstraint(
            "membership_id",
            "permission_id",
            name="uq_membership_permission",
        ),
    )

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
