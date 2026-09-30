from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.driver import Driver
from app.models.truck import Truck
from app.schemas.truck import TruckCreate, TruckRead

router = APIRouter(tags=["Trucks"])


def truck_response(truck: Truck) -> dict:
    return {
        **{
            column.name: getattr(truck, column.name)
            for column in Truck.__table__.columns
        },
        "driver_name": truck.driver.name if truck.driver else None,
        "driver_company_name": (
            truck.driver.company_name if truck.driver else None
        ),
    }


def validate_driver(
    driver_id: int | None,
    truck_id: int | None,
    db: Session,
) -> Driver | None:
    if driver_id is None:
        return None

    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    existing_truck = (
        db.query(Truck)
        .filter(
            Truck.driver_id == driver_id,
            Truck.id != truck_id,
        )
        .first()
    )

    if existing_truck is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Driver is already assigned to truck {existing_truck.unit_number}",
        )

    return driver


@router.post(
    "/trucks/",
    response_model=TruckRead,
    summary="Create Truck",
)
def create_truck(truck: TruckCreate, db: Session = Depends(get_db)):
    validate_driver(truck.driver_id, None, db)

    db_truck = Truck(**truck.model_dump())

    db.add(db_truck)
    db.commit()
    db.refresh(db_truck)

    return truck_response(db_truck)


@router.get(
    "/trucks/",
    response_model=list[TruckRead],
    summary="View All Trucks",
)
def read_trucks(db: Session = Depends(get_db)):
    trucks = db.query(Truck).all()
    return [truck_response(truck) for truck in trucks]


@router.get(
    "/trucks/{truck_id}",
    response_model=TruckRead,
    summary="View Truck",
)
def read_truck(truck_id: int, db: Session = Depends(get_db)):
    truck = db.query(Truck).filter(Truck.id == truck_id).first()

    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    return truck_response(truck)


@router.put(
    "/trucks/{truck_id}",
    response_model=TruckRead,
    summary="Update Truck",
)
def update_truck(
    truck_id: int,
    truck_update: TruckCreate,
    db: Session = Depends(get_db),
):
    truck = db.query(Truck).filter(Truck.id == truck_id).first()

    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    validate_driver(truck_update.driver_id, truck_id, db)

    for key, value in truck_update.model_dump().items():
        setattr(truck, key, value)

    db.commit()
    db.refresh(truck)

    return truck_response(truck)


@router.post(
    "/trucks/{truck_id}/assign-driver/{driver_id}",
    response_model=TruckRead,
    summary="Assign Driver to Truck",
)
def assign_driver(
    truck_id: int,
    driver_id: int,
    db: Session = Depends(get_db),
):
    truck = db.query(Truck).filter(Truck.id == truck_id).first()

    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    validate_driver(driver_id, truck_id, db)

    truck.driver_id = driver_id

    db.commit()
    db.refresh(truck)

    return truck_response(truck)


@router.post(
    "/trucks/{truck_id}/unassign-driver",
    response_model=TruckRead,
    summary="Unassign Driver from Truck",
)
def unassign_driver(
    truck_id: int,
    db: Session = Depends(get_db),
):
    truck = db.query(Truck).filter(Truck.id == truck_id).first()

    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    truck.driver_id = None

    db.commit()
    db.refresh(truck)

    return truck_response(truck)


@router.delete(
    "/trucks/{truck_id}",
    summary="Delete Truck",
)
def delete_truck(
    truck_id: int,
    delete_driver: bool = False,
    db: Session = Depends(get_db),
):
    truck = db.query(Truck).filter(Truck.id == truck_id).first()

    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    driver = truck.driver

    if delete_driver and driver is not None:
        db.delete(driver)

    db.delete(truck)
    db.commit()

    return {
        "message": "Truck deleted successfully",
        "driver_deleted": bool(delete_driver and driver is not None),
    }
