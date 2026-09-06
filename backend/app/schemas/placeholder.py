# schemas/placeholder.py
# Placeholder for schema files
# Safe to import before creating real Pydantic schemas
from pydantic import BaseModel
class PlaceholderSchema(BaseModel):
    name: str = "Placeholder"
