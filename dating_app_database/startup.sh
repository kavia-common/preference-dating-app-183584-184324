#!/bin/bash
set -euo pipefail

# Guardrail: This script must run from /opt/dating_app_database and must not reference 'db_visualizer'.
# PostgreSQL startup script with init, config for 0.0.0.0:5001, and readiness probe
DB_NAME="${POSTGRES_DB:-myapp}"
DB_USER="${POSTGRES_USER:-appuser}"
DB_PASSWORD="${POSTGRES_PASSWORD:-dbuser123}"
DB_PORT="${POSTGRES_PORT:-5001}"
DEFAULT_PGDATA="${PGDATA:-/var/lib/postgresql/data}"

echo "Starting PostgreSQL setup on port ${DB_PORT} ..."

# Locate postgres binaries
PG_VERSION=$(ls /usr/lib/postgresql/ | head -1)
PG_BIN="/usr/lib/postgresql/${PG_VERSION}/bin"
echo "Detected PostgreSQL version: ${PG_VERSION} (bin: ${PG_BIN})"

# Determine a writable PGDATA directory:
# Prefer $PGDATA if set and writable; otherwise fallback to local ./pgdata under repo
FALLBACK_PGDATA="$(pwd)/pgdata"
PGDATA_DIR="${DEFAULT_PGDATA}"

ensure_dir() {
  local dir="$1"
  mkdir -p "$dir" || true
}

is_writable_dir() {
  local dir="$1"
  [ -d "$dir" ] && [ -w "$dir" ]
}

# Ensure chosen PGDATA is writable, else fallback
ensure_dir "${PGDATA_DIR}"
if ! is_writable_dir "${PGDATA_DIR}"; then
  echo "Notice: ${PGDATA_DIR} is not writable in this environment. Falling back to ${FALLBACK_PGDATA}"
  PGDATA_DIR="${FALLBACK_PGDATA}"
  ensure_dir "${PGDATA_DIR}"
fi

echo "Using PGDATA=${PGDATA_DIR}"

# Attempt to set permissions if possible; skip if not permitted
set_perms() {
  local target="$1"
  if command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
    sudo chown -R postgres:postgres "${target}" || true
    sudo chmod 700 "${target}" || true
  else
    chmod 700 "${target}" || true
  fi
}
set_perms "${PGDATA_DIR}"

# Helper to run a command as postgres user if possible; otherwise run directly
run_as_postgres() {
  if command -v sudo >/dev/null 2>&1; then
    sudo -u postgres "$@" 2>/dev/null || "$@"
  else
    "$@"
  fi
}

# If PGDATA is empty (no PG_VERSION), initialize it
if [ ! -f "${PGDATA_DIR}/PG_VERSION" ]; then
  echo "PGDATA empty. Initializing database cluster at ${PGDATA_DIR} ..."
  run_as_postgres "${PG_BIN}/initdb" -D "${PGDATA_DIR}"

  # Configure pg_hba.conf for local md5/scram and host connections
  echo "Configuring pg_hba.conf ..."
  cat > "${PGDATA_DIR}/pg_hba.conf" <<HBA
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     trust
host    all             all             127.0.0.1/32            md5
host    all             all             0.0.0.0/0               md5
host    all             all             ::1/128                 md5
HBA

  # Attempt ownership set; ignore if not permitted
  if command -v sudo >/dev/null 2>&1; then
    sudo chown postgres:postgres "${PGDATA_DIR}/pg_hba.conf" 2>/dev/null || true
  fi
fi

# Start postgres with explicit port and listen_addresses for 0.0.0.0
echo "Starting PostgreSQL server (listen_addresses='*', port=${DB_PORT}) ..."
run_as_postgres "${PG_BIN}/postgres" -D "${PGDATA_DIR}" -p "${DB_PORT}" -c listen_addresses='*' &

# Readiness: wait for server to accept connections
echo "Waiting for PostgreSQL to accept connections ..."
for i in $(seq 1 60); do
  if run_as_postgres "${PG_BIN}/pg_isready" -h 127.0.0.1 -p "${DB_PORT}" -d "${DB_NAME}" -U "${DB_USER}" >/dev/null 2>&1; then
    echo "pg_isready succeeded (host=127.0.0.1 port=${DB_PORT} db=${DB_NAME} user=${DB_USER})."
    break
  fi

  # Fallback check to generic readiness if db/user don't exist yet
  if run_as_postgres "${PG_BIN}/pg_isready" -h 127.0.0.1 -p "${DB_PORT}" >/dev/null 2>&1; then
    echo "Server accepting connections; proceeding with DB/user creation ..."
    break
  fi

  echo "Waiting for PostgreSQL... (${i}/60)"
  sleep 1
done

# Ensure role and database exist (idempotent)
echo "Creating role '${DB_USER}' and database '${DB_NAME}' if needed ..."
run_as_postgres "${PG_BIN}/psql" -p "${DB_PORT}" -d postgres <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}') THEN
    EXECUTE format('CREATE ROLE %I WITH LOGIN PASSWORD %L', '${DB_USER}', '${DB_PASSWORD}');
  ELSE
    EXECUTE format('ALTER ROLE %I WITH LOGIN PASSWORD %L', '${DB_USER}', '${DB_PASSWORD}');
  END IF;
END
\$\$;
SQL

# Create database if not exists
if ! run_as_postgres "${PG_BIN}/psql" -p "${DB_PORT}" -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1; then
  run_as_postgres "${PG_BIN}/createdb" -p "${DB_PORT}" "${DB_NAME}"
fi

# Grant privileges and ensure schema access in target DB
run_as_postgres "${PG_BIN}/psql" -p "${DB_PORT}" -d "${DB_NAME}" <<SQL
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
GRANT USAGE, CREATE ON SCHEMA public TO ${DB_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${DB_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${DB_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO ${DB_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO ${DB_USER};
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${DB_USER};
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${DB_USER};
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO ${DB_USER};
SQL

# Final readiness loop with exact target DB/user
echo "Verifying readiness with pg_isready for db=${DB_NAME} user=${DB_USER} ..."
READY=0
for i in $(seq 1 60); do
  if run_as_postgres "${PG_BIN}/pg_isready" -h 127.0.0.1 -p "${DB_PORT}" -d "${DB_NAME}" -U "${DB_USER}" >/dev/null 2>&1; then
    echo "PostgreSQL ready."
    READY=1
    break
  fi
  sleep 1
done

if [ "${READY}" -ne 1 ]; then
  echo "PostgreSQL did not become ready in time."
  exit 1
fi

# Update connection helper file
echo "psql postgresql://${DB_USER}:${DB_PASSWORD}@localhost:${DB_PORT}/${DB_NAME}" > db_connection.txt

echo "Configuration complete."
echo "Database: ${DB_NAME}"
echo "User: ${DB_USER}"
echo "Port: ${DB_PORT}"
echo "Connection helper saved to db_connection.txt"
