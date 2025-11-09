from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from . import models


# PUBLIC_INTERFACE
def create_profile(db: Session, data: dict) -> models.Profile:
    """Create a new profile record."""
    obj = models.Profile(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# PUBLIC_INTERFACE
def get_profile(db: Session, profile_id: int) -> Optional[models.Profile]:
    """Fetch profile by primary key."""
    return db.get(models.Profile, profile_id)


# PUBLIC_INTERFACE
def update_profile(db: Session, profile_id: int, updates: dict) -> Optional[models.Profile]:
    """Update a profile; returns updated object or None if not found."""
    obj = db.get(models.Profile, profile_id)
    if not obj:
        return None
    for k, v in updates.items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# PUBLIC_INTERFACE
def delete_profile(db: Session, profile_id: int) -> bool:
    """Delete profile by id; returns True if deleted."""
    obj = db.get(models.Profile, profile_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# PUBLIC_INTERFACE
def list_profiles_filtered(
    db: Session,
    height_category_id: Optional[int] = None,
    weight_category_id: Optional[int] = None
) -> List[models.Profile]:
    """List profiles filtered by optional height/weight category."""
    stmt = select(models.Profile)

    conditions = []

    if height_category_id is not None:
        hc = db.get(models.HeightCategory, height_category_id)
        if hc:
            if hc.min_cm is not None:
                conditions.append(models.Profile.height_cm >= hc.min_cm)
            if hc.max_cm is not None:
                conditions.append(models.Profile.height_cm <= hc.max_cm)

    if weight_category_id is not None:
        wc = db.get(models.WeightCategory, weight_category_id)
        if wc:
            if wc.min_kg is not None:
                conditions.append(models.Profile.weight_kg >= wc.min_kg)
            if wc.max_kg is not None:
                conditions.append(models.Profile.weight_kg <= wc.max_kg)

    if conditions:
        stmt = stmt.where(and_(*conditions))

    return list(db.scalars(stmt).all())


# PUBLIC_INTERFACE
def get_height_categories(db: Session) -> List[models.HeightCategory]:
    """Return all height categories ordered by min."""
    stmt = select(models.HeightCategory).order_by(models.HeightCategory.min_cm.asc().nullsfirst())
    return list(db.scalars(stmt).all())


# PUBLIC_INTERFACE
def get_weight_categories(db: Session) -> List[models.WeightCategory]:
    """Return all weight categories ordered by min."""
    stmt = select(models.WeightCategory).order_by(models.WeightCategory.min_kg.asc().nullsfirst())
    return list(db.scalars(stmt).all())
