from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.driver import Driver
from app.models.truck import Truck
from app.schemas.driver import DriverCreate, DriverRead

router = APIRouter(tags=["Drivers"])


def driver_response(driver: Driver) -> dict:
    return {
        **{
            column.name: getattr(driver, column.name)
            for column in Driver.__table__.columns
        },
        "truck_id": driver.truck.id if driver.truck else None,
        "truck_unit_number": driver.truck.unit_number if driver.truck else None,
    }


@router.post("/drivers/", response_model=DriverRead, summary="Create Driver")
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    db_driver = Driver(**driver.model_dump())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return driver_response(db_driver)


@router.get("/drivers/", response_model=list[DriverRead], summary="View All Drivers")
def get_drivers(db: Session = Depends(get_db)):
    drivers = db.query(Driver).all()
    return [driver_response(driver) for driver in drivers]


@router.get("/drivers/{driver_id}", response_model=DriverRead, summary="View Driver")
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    return driver_response(driver)


@router.put("/drivers/{driver_id}", response_model=DriverRead, summary="Update Driver")
def update_driver(
    driver_id: int,
    driver_data: DriverCreate,
    db: Session = Depends(get_db),
):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    for key, value in driver_data.model_dump().items():
        setattr(driver, key, value)

    db.commit()
    db.refresh(driver)

    return driver_response(driver)


@router.delete("/drivers/{driver_id}", summary="Delete Driver")
def delete_driver(driver_id: int, delete_truck: bool = False, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    truck = driver.truck

    if delete_truck and truck is not None:
        db.delete(truck)

    db.delete(driver)
    db.commit()

    return {
        "message": "Driver deleted successfully",
        "truck_deleted": bool(delete_truck and truck is not None),
    }
