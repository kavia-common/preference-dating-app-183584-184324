# Database schema setup for Preference Dating App (PostgreSQL)

Use the db_connection.txt connection string. Execute each SQL statement one at a time as separate commands.

Connection:
- From repo root:
  psql postgresql://appuser:dbuser123@localhost:5001/myapp

Tables (run each as a separate -c):

1) auth_user
CREATE TABLE IF NOT EXISTS auth_user (
  id SERIAL PRIMARY KEY,
  username VARCHAR(150) UNIQUE NOT NULL,
  email VARCHAR(254) NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  date_joined TIMESTAMPTZ DEFAULT NOW()
);

2) core_profile
CREATE TABLE IF NOT EXISTS core_profile (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  display_name VARCHAR(100) NOT NULL,
  bio TEXT NOT NULL,
  height_cm INTEGER NULL,
  weight_kg INTEGER NULL,
  photo_url VARCHAR(200) NOT NULL,
  gender VARCHAR(32) NOT NULL,
  interests JSONB NOT NULL DEFAULT '{}'::jsonb,
  user_id INTEGER UNIQUE NOT NULL REFERENCES auth_user(id)
);

3) core_match
CREATE TABLE IF NOT EXISTS core_match (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE,
  matched_at TIMESTAMPTZ DEFAULT NOW(),
  user_a_id INTEGER NOT NULL REFERENCES auth_user(id),
  user_b_id INTEGER NOT NULL REFERENCES auth_user(id)
);

4) core_message
CREATE TABLE IF NOT EXISTS core_message (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  content TEXT NOT NULL,
  sent_at TIMESTAMPTZ DEFAULT NOW(),
  is_read BOOLEAN DEFAULT FALSE,
  match_id BIGINT NOT NULL REFERENCES core_match(id),
  sender_id INTEGER NOT NULL REFERENCES auth_user(id)
);

5) core_filterpreset
CREATE TABLE IF NOT EXISTS core_filterpreset (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  name VARCHAR(100) NOT NULL,
  min_height_cm INTEGER NULL,
  max_height_cm INTEGER NULL,
  min_weight_kg INTEGER NULL,
  max_weight_kg INTEGER NULL,
  genders JSONB NOT NULL DEFAULT '[]'::jsonb,
  is_public BOOLEAN DEFAULT TRUE,
  owner_id INTEGER NULL REFERENCES auth_user(id)
);

Indexes (each as separate -c):
CREATE INDEX IF NOT EXISTS idx_profile_height_cm ON core_profile (height_cm);
CREATE INDEX IF NOT EXISTS idx_profile_weight_kg ON core_profile (weight_kg);
CREATE INDEX IF NOT EXISTS idx_profile_gender ON core_profile (gender);
CREATE INDEX IF NOT EXISTS idx_match_user_a ON core_match (user_a_id);
CREATE INDEX IF NOT EXISTS idx_match_user_b ON core_match (user_b_id);
CREATE INDEX IF NOT EXISTS idx_message_match_id ON core_message (match_id);
CREATE INDEX IF NOT EXISTS idx_message_sender_id ON core_message (sender_id);

Seed data (each INSERT separately as its own -c):
-- demo users
INSERT INTO auth_user (username, email) VALUES ('demo','demo@example.com') ON CONFLICT (username) DO NOTHING;
INSERT INTO auth_user (username, email) VALUES ('alex','alex@example.com') ON CONFLICT (username) DO NOTHING;
INSERT INTO auth_user (username, email) VALUES ('blake','blake@example.com') ON CONFLICT (username) DO NOTHING;

-- profiles (use subselects to resolve user ids)
INSERT INTO core_profile (display_name,bio,height_cm,weight_kg,photo_url,gender,interests,user_id)
SELECT 'Demo','Love travel and food.',172,70,'https://images.unsplash.com/photo-1502685104226-ee32379fefbe','female','{"tags":["travel","food","music"]}', id FROM auth_user WHERE username='demo'
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO core_profile (display_name,bio,height_cm,weight_kg,photo_url,gender,interests,user_id)
SELECT 'Alex','Outdoors and hiking.',180,82,'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d','male','{"tags":["hiking","outdoors","coffee"]}', id FROM auth_user WHERE username='alex'
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO core_profile (display_name,bio,height_cm,weight_kg,photo_url,gender,interests,user_id)
SELECT 'Blake','Tech and art.',165,60,'https://images.unsplash.com/photo-1544005313-94ddf0286df2','nonbinary','{"tags":["tech","art","gaming"]}', id FROM auth_user WHERE username='blake'
ON CONFLICT (user_id) DO NOTHING;

-- presets
INSERT INTO core_filterpreset (name,min_height_cm,max_height_cm,min_weight_kg,max_weight_kg,genders,is_public)
VALUES ('Short & Light', NULL, 165, NULL, 60, '["female","nonbinary"]', TRUE)
ON CONFLICT DO NOTHING;

INSERT INTO core_filterpreset (name,min_height_cm,max_height_cm,min_weight_kg,max_weight_kg,genders,is_public)
VALUES ('Tall & Active', 175, NULL, 70, NULL, '["male"]', TRUE)
ON CONFLICT DO NOTHING;

Notes:
- Execute via: psql postgresql://appuser:dbuser123@localhost:5001/myapp -c "SQL_HERE"
- Ensure each statement is executed individually.
