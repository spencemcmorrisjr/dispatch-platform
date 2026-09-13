from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.truck import Truck
from app.schemas.truck import TruckCreate, TruckRead


router = APIRouter()


@router.post("/trucks/", response_model=TruckRead)
def create_truck(truck: TruckCreate, db: Session = Depends(get_db)):
    db_truck = Truck(
        unit_number=truck.unit_number,
        vin=truck.vin,
        year=truck.year,
        make=truck.make,
        model=truck.model,
        license_plate=truck.license_plate,
        dot_inspection_expiration=truck.dot_inspection_expiration,
        insurance_expiration=truck.insurance_expiration,
        status=truck.status,
        driver_id=truck.driver_id,
    )

    db.add(db_truck)
    db.commit()
    db.refresh(db_truck)

    return db_truck


@router.get("/trucks/", response_model=list[TruckRead])
def read_trucks(db: Session = Depends(get_db)):
    return db.query(Truck).all()


@router.get("/trucks/{truck_id}", response_model=TruckRead)
def read_truck(truck_id: int, db: Session = Depends(get_db)):
    truck = db.query(Truck).filter(Truck.id == truck_id).first()

    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    return truck


@router.put("/trucks/{truck_id}", response_model=TruckRead)
def update_truck(
    truck_id: int,
    truck_update: TruckCreate,
    db: Session = Depends(get_db),
):
    truck = db.query(Truck).filter(Truck.id == truck_id).first()

    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    truck.unit_number = truck_update.unit_number
    truck.vin = truck_update.vin
    truck.year = truck_update.year
    truck.make = truck_update.make
    truck.model = truck_update.model
    truck.license_plate = truck_update.license_plate
    truck.dot_inspection_expiration = truck_update.dot_inspection_expiration
    truck.insurance_expiration = truck_update.insurance_expiration
    truck.status = truck_update.status
    truck.driver_id = truck_update.driver_id

    db.commit()
    db.refresh(truck)

    return truck


@router.delete("/trucks/{truck_id}")
def delete_truck(truck_id: int, db: Session = Depends(get_db)):
    truck = db.query(Truck).filter(Truck.id == truck_id).first()

    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    db.delete(truck)
    db.commit()

    return {"message": "Truck deleted successfully"}