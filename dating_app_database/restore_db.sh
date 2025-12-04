#!/usr/bin/env bash
set -euo pipefail
# Guardrail: Do not assume any subdirectory like 'db_visualizer'; run from current working directory.

PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-postgres}"
PGDATABASE="${PGDATABASE:-postgres}"
BACKUP_FILE="${1:-}"

if [[ -z "${BACKUP_FILE}" ]]; then
  echo "Usage: $0 <backup_file.sql.gz>"
  exit 1
fi

echo "Restoring backup from ${BACKUP_FILE}"
gunzip -c "${BACKUP_FILE}" | psql -h "${PGHOST}" -p "${PGPORT}" -U "${PGUSER}" -d "${PGDATABASE}"
echo "Restore complete."
