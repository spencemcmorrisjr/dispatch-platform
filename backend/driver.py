from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.driver import DriverCreate, DriverRead
from app.models.driver import Driver
from app.database import get_db  # We will create this next

router = APIRouter()

@router.post("/drivers/", response_model=DriverRead)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    db_driver = Driver(name=driver.name, phone=driver.phone)
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver