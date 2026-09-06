from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.driver import DriverCreate, DriverRead
from app.models.driver import Driver
from app.database import get_db

router = APIRouter()


# CREATE DRIVER
@router.post("/drivers/", response_model=DriverRead)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):

    db_driver = Driver(
        name=driver.name,
        phone=driver.phone,
        email=driver.email,
        cdl_number=driver.cdl_number,
        license_expiration=driver.license_expiration,
        medical_card_expiration=driver.medical_card_expiration,
        preferred_lanes=driver.preferred_lanes,
        home_time=driver.home_time,
        no_go_states=driver.no_go_states,
        status=driver.status
    )

    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)

    return db_driver


# READ ALL DRIVERS
@router.get("/drivers/", response_model=list[DriverRead])
def read_drivers(db: Session = Depends(get_db)):

    drivers = db.query(Driver).all()

    return drivers


# READ ONE DRIVER
@router.get("/drivers/{driver_id}", response_model=DriverRead)
def read_driver(driver_id: int, db: Session = Depends(get_db)):

    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if driver is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return driver


# UPDATE DRIVER
@router.put("/drivers/{driver_id}", response_model=DriverRead)
def update_driver(
    driver_id: int,
    driver_update: DriverCreate,
    db: Session = Depends(get_db)
):

    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if driver is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    driver.name = driver_update.name
    driver.phone = driver_update.phone
    driver.email = driver_update.email
    driver.cdl_number = driver_update.cdl_number
    driver.license_expiration = driver_update.license_expiration
    driver.medical_card_expiration = driver_update.medical_card_expiration
    driver.preferred_lanes = driver_update.preferred_lanes
    driver.home_time = driver_update.home_time
    driver.no_go_states = driver_update.no_go_states
    driver.status = driver_update.status

    db.commit()
    db.refresh(driver)

    return driver


# DELETE DRIVER
@router.delete("/drivers/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db)):

    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if driver is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    db.delete(driver)
    db.commit()

    return {
        "message": "Driver deleted successfully"
    }