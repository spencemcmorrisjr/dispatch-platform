from sqlalchemy import Boolean, Column, Integer, String, Text
from app.database import Base


class TrainingModule(Base):
    __tablename__ = "training_modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    active = Column(Boolean, nullable=False, default=True)
