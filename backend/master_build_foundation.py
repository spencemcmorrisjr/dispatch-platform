from pathlib import Path

ROOT = Path("app")

folders = [
    "models",
    "schemas",
    "routes",
    "services",
    "permissions",
    "utils",
]

for folder in folders:
    (ROOT / folder).mkdir(parents=True, exist_ok=True)

files = {
    "app/services/__init__.py": "",
    "app/permissions/__init__.py": "",
    "app/utils/__init__.py": "",

    "app/models/membership.py": '''from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.database import Base


class BusinessMembership(Base):
    __tablename__ = "business_memberships"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    user_id = Column(Integer, nullable=False, index=True)

    role = Column(String(50), nullable=False, default="driver")
    active = Column(Boolean, nullable=False, default=True)
''',

    "app/models/permission.py": '''from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
''',

    "app/models/audit.py": '''from sqlalchemy import Column, DateTime, Integer, String, Text, func
from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)

    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True)

    reason = Column(Text, nullable=True)
    previous_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
''',

    "app/models/document.py": '''from sqlalchemy import Column, DateTime, Integer, String, Text, func
from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=True, index=True)
    driver_id = Column(Integer, nullable=True, index=True)
    load_id = Column(Integer, nullable=True, index=True)

    document_type = Column(String(100), nullable=False)
    file_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="unpaid")
    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
''',

    "app/models/communication.py": '''from sqlalchemy import Column, DateTime, Integer, String, Text, func
from app.database import Base


class CommunicationTimeline(Base):
    __tablename__ = "communication_timeline"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=True, index=True)
    load_id = Column(Integer, nullable=True, index=True)
    driver_id = Column(Integer, nullable=True, index=True)

    communication_type = Column(String(50), nullable=False)
    direction = Column(String(20), nullable=True)
    subject = Column(String(255), nullable=True)
    message = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
''',

    "app/models/exception_item.py": '''from sqlalchemy import Column, DateTime, Integer, String, Text, func
from app.database import Base


class ExceptionItem(Base):
    __tablename__ = "exception_items"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=True, index=True)
    load_id = Column(Integer, nullable=True, index=True)
    driver_id = Column(Integer, nullable=True, index=True)

    exception_type = Column(String(100), nullable=False)
    severity = Column(String(30), nullable=False, default="warning")
    status = Column(String(30), nullable=False, default="open")
    description = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
''',

    "app/models/training.py": '''from sqlalchemy import Boolean, Column, Integer, String, Text
from app.database import Base


class TrainingModule(Base):
    __tablename__ = "training_modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    active = Column(Boolean, nullable=False, default=True)
''',

    "app/models/maintenance.py": '''from sqlalchemy import Column, Date, Integer, String, Text
from app.database import Base


class MaintenanceItem(Base):
    __tablename__ = "maintenance_items"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=True, index=True)
    truck_id = Column(Integer, nullable=True, index=True)

    maintenance_type = Column(String(100), nullable=False)
    due_date = Column(Date, nullable=True)
    mileage_due = Column(Integer, nullable=True)
    status = Column(String(30), nullable=False, default="scheduled")
    notes = Column(Text, nullable=True)
''',

    "app/models/vendor.py": '''from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=True, index=True)

    name = Column(String(200), nullable=False)
    vendor_type = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
''',

    "app/models/__init__.py": '''from app.models.business import Business
from app.models.membership import BusinessMembership
from app.models.permission import Permission
from app.models.audit import AuditLog
from app.models.document import Document
from app.models.communication import CommunicationTimeline
from app.models.exception_item import ExceptionItem
from app.models.training import TrainingModule
from app.models.maintenance import MaintenanceItem
from app.models.vendor import Vendor

__all__ = [
    "Business",
    "BusinessMembership",
    "Permission",
    "AuditLog",
    "Document",
    "CommunicationTimeline",
    "ExceptionItem",
    "TrainingModule",
    "MaintenanceItem",
    "Vendor",
]
''',
}

for relative_path, content in files.items():
    path = Path(relative_path)

    # Never overwrite existing files except models/__init__.py,
    # which is intentionally updated to register the new models.
    if path.exists() and path.as_posix() != "app/models/__init__.py":
        print(f"SKIPPED existing: {path}")
        continue

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"CREATED: {path}")

print()
print("MASTER BUILD FOUNDATION COMPLETE")
