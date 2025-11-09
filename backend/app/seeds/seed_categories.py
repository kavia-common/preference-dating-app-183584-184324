"""
Seed script to insert preset height and weight categories.
Run with: python -m app.seeds.seed_categories
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import engine, SessionLocal
from .. import models

HEIGHT_PRESETS = [
    {"name": "Shortest", "min_cm": None, "max_cm": 150},
    {"name": "Short", "min_cm": 151, "max_cm": 165},
    {"name": "Average", "min_cm": 166, "max_cm": 180},
    {"name": "Tall", "min_cm": 181, "max_cm": 195},
    {"name": "Tallest", "min_cm": 196, "max_cm": None},
]

WEIGHT_PRESETS = [
    {"name": "Lightest", "min_kg": None, "max_kg": 50},
    {"name": "Light", "min_kg": 51, "max_kg": 65},
    {"name": "Average", "min_kg": 66, "max_kg": 80},
    {"name": "Heavy", "min_kg": 81, "max_kg": 100},
    {"name": "Heaviest", "min_kg": 101, "max_kg": None},
]


def upsert_height_categories(db: Session):
    existing = {hc.name for hc in db.scalars(select(models.HeightCategory)).all()}
    for preset in HEIGHT_PRESETS:
        if preset["name"] in existing:
            continue
        db.add(models.HeightCategory(**preset))
    db.commit()


def upsert_weight_categories(db: Session):
    existing = {wc.name for wc in db.scalars(select(models.WeightCategory)).all()}
    for preset in WEIGHT_PRESETS:
        if preset["name"] in existing:
            continue
        db.add(models.WeightCategory(**preset))
    db.commit()


def main():
    # Ensure metadata exists (alembic migration creates these tables; this is a safety fallback)
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        upsert_height_categories(db)
        upsert_weight_categories(db)
        print("✓ Seeded height and weight categories.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
