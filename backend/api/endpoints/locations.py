from api.utils.security import validate_token
from core.database import get_db as db
from fastapi import APIRouter, Depends, HTTPException
from models.location_type import LocationType
from sqlalchemy.orm import Session


router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/location-types/")
def list_location_types(db: Session = Depends(db), _: None = Depends(validate_token)):
    items = db.query(LocationType).all()
    return items


@router.get("/location-types/{location_type_id}/")
def detail_location_types(
    location_type_id: int, db: Session = Depends(db), _: None = Depends(validate_token)
):
    location_type = (
        db.query(LocationType).filter(LocationType.id == location_type_id).first()
    )
    if location_type is None:
        raise HTTPException(status_code=404, detail="Location type not found")
    return location_type
