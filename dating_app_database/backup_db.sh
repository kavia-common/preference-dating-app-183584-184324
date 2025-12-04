#!/usr/bin/env bash
set -euo pipefail
# Guardrail: Do not assume any subdirectory like 'db_visualizer'; run from current working directory.

PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-postgres}"
PGDATABASE="${PGDATABASE:-postgres}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"

mkdir -p "${BACKUP_DIR}"
ts=$(date +"%Y%m%d_%H%M%S")
echo "Creating backup ${BACKUP_DIR}/backup_${ts}.sql.gz"
pg_dump -h "${PGHOST}" -p "${PGPORT}" -U "${PGUSER}" -d "${PGDATABASE}" | gzip > "${BACKUP_DIR}/backup_${ts}.sql.gz"
echo "Backup complete."
