#!/bin/bash
set -euo pipefail

# Move to working directory where startup.sh was copied
cd /opt/dating_app_database

# Run the PostgreSQL startup and initialization
./startup.sh

# Keep the container running and tail postgres logs if available
# The startup.sh launches postgres in background, so we wait here.
# Fallback to a simple sleep loop if no logs.
LOG_FILE="/var/lib/postgresql/data/log/postgresql.log"
if [ -f "$LOG_FILE" ]; then
  tail -F "$LOG_FILE"
else
  echo "PostgreSQL started. Entering wait loop to keep container alive."
  while true; do sleep 60; done
fi
