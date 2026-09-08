"""API routes for Public Listings."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db
from app.models.property import Property
from app.models.unit import Unit
from app.schemas.listing import PropertyListing, UnitListing

router = APIRouter()

@router.get("/", response_model=List[PropertyListing])
def get_public_listings(db: Session = Depends(get_db)):
    """Fetch all properties that have at least one vacant unit."""
    # Find properties that have vacant units
    stmt = select(Property).join(Unit).where(Unit.status == "vacant").distinct()
    properties = db.scalars(stmt).all()
    
    # We need to construct the response manually to filter units,
    # because property.units returns ALL units, not just vacant ones.
    result = []
    for p in properties:
        vacant_units = [u for u in p.units if u.status == "vacant"]
        if vacant_units:
            unit_listings = [
                UnitListing.model_validate(u) for u in vacant_units
            ]
            prop_listing = PropertyListing(
                id=p.id,
                name=p.name,
                address=p.address,
                city=p.city,
                state=p.state,
                zip_code=p.zip_code,
                property_type=p.property_type,
                image_url=p.image_url,
                units=unit_listings
            )
            result.append(prop_listing)
            
    return result

@router.get("/{id}", response_model=PropertyListing)
def get_public_listing(id: int, db: Session = Depends(get_db)):
    """Fetch a specific property listing."""
    p = db.get(Property, id)
    if not p:
        raise HTTPException(status_code=404, detail="Property not found")
        
    vacant_units = [u for u in p.units if u.status == "vacant"]
    if not vacant_units:
        raise HTTPException(status_code=404, detail="No vacant units at this property")
        
    unit_listings = [UnitListing.model_validate(u) for u in vacant_units]
    return PropertyListing(
        id=p.id,
        name=p.name,
        address=p.address,
        city=p.city,
        state=p.state,
        zip_code=p.zip_code,
        property_type=p.property_type,
        image_url=p.image_url,
        units=unit_listings
    )
