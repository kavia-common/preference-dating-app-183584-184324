import os
from datetime import datetime
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL") or f"postgresql://{os.getenv('PGUSER','appuser')}:{os.getenv('PGPASSWORD','dbuser123')}@{os.getenv('PGHOST','localhost')}:{int(os.getenv('PGPORT','5001'))}/{os.getenv('PGDATABASE','myapp')}"
engine = create_engine(DATABASE_URL, future=True)

USERS = [
    {"id": 1001, "username": "alice", "email": "alice@example.com"},
    {"id": 1002, "username": "bob", "email": "bob@example.com"},
    {"id": 1003, "username": "carol", "email": "carol@example.com"},
]

PROFILES = [
    {"display_name": "Alice", "bio": "Traveler & foodie.", "height_cm": 165, "weight_kg": 58, "photo_url": "https://picsum.photos/seed/al/400/600", "gender": "female", "interests": {"tags": ["travel", "food"]}, "user_id": 1001},
    {"display_name": "Bob", "bio": "Hiking and tech.", "height_cm": 178, "weight_kg": 76, "photo_url": "https://picsum.photos/seed/bb/400/600", "gender": "male", "interests": {"tags": ["hiking", "coding"]}, "user_id": 1002},
    {"display_name": "Carol", "bio": "Art & coffee dates.", "height_cm": 170, "weight_kg": 65, "photo_url": "https://picsum.photos/seed/cc/400/600", "gender": "female", "interests": {"tags": ["art", "coffee"]}, "user_id": 1003},
]

PRESETS = [
    {"name": "Short & Light", "min_height_cm": None, "max_height_cm": 165, "min_weight_kg": None, "max_weight_kg": 60, "genders": ["female"], "is_public": True},
    {"name": "Tall", "min_height_cm": 180, "max_height_cm": None, "min_weight_kg": None, "max_weight_kg": None, "genders": [], "is_public": True},
]

def run():
    with engine.begin() as conn:
        # Users
        for u in USERS:
            conn.execute(text("""
                INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
                VALUES (:id, '', NULL, false, :username, '', '', :email, false, true, NOW())
                ON CONFLICT (id) DO NOTHING
            """), u)
        # Profiles
        for p in PROFILES:
            conn.execute(text("""
                INSERT INTO core_profile (created_at, updated_at, display_name, bio, height_cm, weight_kg, photo_url, gender, interests, user_id)
                VALUES (NOW(), NOW(), :display_name, :bio, :height_cm, :weight_kg, :photo_url, :gender, :interests::jsonb, :user_id)
                ON CONFLICT (user_id) DO NOTHING
            """), {"display_name": p["display_name"], "bio": p["bio"], "height_cm": p["height_cm"], "weight_kg": p["weight_kg"], "photo_url": p["photo_url"], "gender": p["gender"], "interests": str(p["interests"]).replace("'", '"'), "user_id": p["user_id"]})
        # Presets
        for f in PRESETS:
            conn.execute(text("""
                INSERT INTO core_filterpreset (created_at, updated_at, name, min_height_cm, max_height_cm, min_weight_kg, max_weight_kg, genders, is_public, owner_id)
                VALUES (NOW(), NOW(), :name, :min_height_cm, :max_height_cm, :min_weight_kg, :max_weight_kg, :genders::jsonb, :is_public, NULL)
                ON CONFLICT DO NOTHING
            """), {"name": f["name"], "min_height_cm": f["min_height_cm"], "max_height_cm": f["max_height_cm"], "min_weight_kg": f["min_weight_kg"], "max_weight_kg": f["max_weight_kg"], "genders": str(f["genders"]).replace("'", '"'), "is_public": f["is_public"]})
    print("✓ Seed complete")

if __name__ == "__main__":
    run()
