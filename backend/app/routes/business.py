from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.business import Business
from app.schemas.business import BusinessCreate, BusinessRead


router = APIRouter(tags=["Businesses"])


@router.post(
    "/businesses/",
    response_model=BusinessRead,
    summary="Create business",
)
def create_business(
    business: BusinessCreate,
    db: Session = Depends(get_db),
):
    db_business = Business(
        name=business.name,
        legal_name=business.legal_name,
        business_type=business.business_type,
        phone=business.phone,
        email=business.email,
    )

    db.add(db_business)
    db.commit()
    db.refresh(db_business)

    return db_business


@router.get(
    "/businesses/",
    response_model=list[BusinessRead],
    summary="View all businesses",
)
def read_businesses(db: Session = Depends(get_db)):
    return db.query(Business).all()


@router.get(
    "/businesses/{business_id}",
    response_model=BusinessRead,
    summary="View 1 business",
)
def read_business(
    business_id: int,
    db: Session = Depends(get_db),
):
    business = db.query(Business).filter(Business.id == business_id).first()

    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")

    return business


@router.put(
    "/businesses/{business_id}",
    response_model=BusinessRead,
    summary="Update business",
)
def update_business(
    business_id: int,
    business_update: BusinessCreate,
    db: Session = Depends(get_db),
):
    business = db.query(Business).filter(Business.id == business_id).first()

    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")

    business.name = business_update.name
    business.legal_name = business_update.legal_name
    business.business_type = business_update.business_type
    business.phone = business_update.phone
    business.email = business_update.email

    db.commit()
    db.refresh(business)

    return business


@router.delete(
    "/businesses/{business_id}",
    summary="Delete business",
)
def delete_business(
    business_id: int,
    db: Session = Depends(get_db),
):
    business = db.query(Business).filter(Business.id == business_id).first()

    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")

    db.delete(business)
    db.commit()

    return {"message": "Business deleted successfully"}
