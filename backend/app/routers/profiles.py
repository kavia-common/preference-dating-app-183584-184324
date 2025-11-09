from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..db import get_db
from .. import crud, schemas, models

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"],
)


@router.post(
    "",
    response_model=schemas.ProfileOut,
    summary="Create a profile",
    description="Create a profile for a given user."
)
def create_profile(payload: schemas.ProfileCreate, db: Session = Depends(get_db)):
    obj = crud.create_profile(db, data=payload.model_dump())
    return obj


@router.get(
    "/{profile_id}",
    response_model=schemas.ProfileOut,
    summary="Get profile by id",
    description="Retrieve a profile by its identifier."
)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    obj = crud.get_profile(db, profile_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Profile not found")
    return obj


@router.put(
    "/{profile_id}",
    response_model=schemas.ProfileOut,
    summary="Update profile",
    description="Update fields on a profile."
)
def update_profile(profile_id: int, payload: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    obj = crud.update_profile(db, profile_id, updates)
    if not obj:
        raise HTTPException(status_code=404, detail="Profile not found")
    return obj


@router.delete(
    "/{profile_id}",
    status_code=204,
    summary="Delete profile",
    description="Delete a profile permanently."
)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_profile(db, profile_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Profile not found")
    return None


@router.get(
    "",
    response_model=List[schemas.ProfileOut],
    summary="List profiles (filtered)",
    description="List candidate profiles filtered by optional height and weight category IDs."
)
def list_profiles(
    height_category_id: Optional[int] = Query(default=None, description="Height category id"),
    weight_category_id: Optional[int] = Query(default=None, description="Weight category id"),
    db: Session = Depends(get_db)
):
    items = crud.list_profiles_filtered(db, height_category_id, weight_category_id)
    return items
