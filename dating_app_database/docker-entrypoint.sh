#!/usr/bin/env bash
set -euo pipefail
# Guardrail: Never cd into any removed subdir like 'db_visualizer'. All scripts run from this fixed WORKDIR.
# Expected WORKDIR inside container: /opt/dating_app_database

exec "$@"
