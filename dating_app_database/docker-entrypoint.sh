#!/bin/bash
set -euo pipefail

# Guardrail: Never cd into any removed subdir like 'db_visualizer'. All scripts run from this fixed WORKDIR.
# Validate and move to working directory where startup.sh was copied
WORKDIR="/opt/dating_app_database"
if [ ! -d "$WORKDIR" ]; then
  echo "Error: Expected working directory '$WORKDIR' does not exist."
  echo "Please ensure the Dockerfile sets WORKDIR correctly and copies scripts there."
  exit 1
fi
cd "$WORKDIR"

# Run the PostgreSQL startup and initialization
if [ ! -x "./startup.sh" ]; then
  echo "Error: startup.sh not found or not executable in $WORKDIR"
  ls -l
  exit 1
fi
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
