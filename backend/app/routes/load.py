from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.load import Load
from app.schemas.load import LoadCreate, LoadRead


router = APIRouter(tags=["Loads"])


@router.post(
    "/loads/",
    response_model=LoadRead,
    summary="Create load",
)
def create_load(load: LoadCreate, db: Session = Depends(get_db)):
    db_load = Load(
        load_number=load.load_number,
        broker_name=load.broker_name,
        pickup_location=load.pickup_location,
        delivery_location=load.delivery_location,
        pickup_date=load.pickup_date,
        delivery_date=load.delivery_date,
        rate=load.rate,
        status=load.status,
        driver_id=load.driver_id,
        truck_id=load.truck_id,
    )

    db.add(db_load)
    db.commit()
    db.refresh(db_load)

    return db_load


@router.get(
    "/loads/",
    response_model=list[LoadRead],
    summary="View all loads",
)
def read_loads(db: Session = Depends(get_db)):
    return db.query(Load).all()


@router.get(
    "/loads/{load_id}",
    response_model=LoadRead,
    summary="View 1 load",
)
def read_load(load_id: int, db: Session = Depends(get_db)):
    load = db.query(Load).filter(Load.id == load_id).first()

    if load is None:
        raise HTTPException(status_code=404, detail="Load not found")

    return load


@router.put(
    "/loads/{load_id}",
    response_model=LoadRead,
    summary="Update load",
)
def update_load(
    load_id: int,
    load_update: LoadCreate,
    db: Session = Depends(get_db),
):
    load = db.query(Load).filter(Load.id == load_id).first()

    if load is None:
        raise HTTPException(status_code=404, detail="Load not found")

    load.load_number = load_update.load_number
    load.broker_name = load_update.broker_name
    load.pickup_location = load_update.pickup_location
    load.delivery_location = load_update.delivery_location
    load.pickup_date = load_update.pickup_date
    load.delivery_date = load_update.delivery_date
    load.rate = load_update.rate
    load.status = load_update.status
    load.driver_id = load_update.driver_id
    load.truck_id = load_update.truck_id

    db.commit()
    db.refresh(load)

    return load


@router.delete(
    "/loads/{load_id}",
    summary="Delete load",
)
def delete_load(load_id: int, db: Session = Depends(get_db)):
    load = db.query(Load).filter(Load.id == load_id).first()

    if load is None:
        raise HTTPException(status_code=404, detail="Load not found")

    db.delete(load)
    db.commit()

    return {"message": "Load deleted successfully"}
