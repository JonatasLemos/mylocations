from core.database import db
from fastapi import APIRouter, HTTPException
from models.location_type import LocationType


router = APIRouter(prefix="/locations")


@router.get("/location-types/")
def list_location_types():
    items = db.query(LocationType).all()
    db.close()
    return items


@router.get("/location-types/{location_type_id}/")
def detail_location_types(location_type_id: int):
    location_type = (
        db.query(LocationType).filter(LocationType.id == location_type_id).first()
    )
    db.close()
    if location_type is None:
        raise HTTPException(status_code=404, detail="Location type not found")
    return location_type
