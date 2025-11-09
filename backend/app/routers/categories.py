from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from .. import crud, schemas

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@router.get(
    "/height",
    response_model=List[schemas.HeightCategoryOut],
    summary="List height categories",
    description="Retrieve all height preset categories."
)
def height_categories(db: Session = Depends(get_db)):
    return crud.get_height_categories(db)

@router.get(
    "/weight",
    response_model=List[schemas.WeightCategoryOut],
    summary="List weight categories",
    description="Retrieve all weight preset categories."
)
def weight_categories(db: Session = Depends(get_db)):
    return crud.get_weight_categories(db)
