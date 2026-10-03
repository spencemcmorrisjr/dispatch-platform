from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.database import Base


class BusinessMembership(Base):
    __tablename__ = "business_memberships"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    user_id = Column(Integer, nullable=False, index=True)

    role = Column(String(50), nullable=False, default="driver")
    active = Column(Boolean, nullable=False, default=True)
