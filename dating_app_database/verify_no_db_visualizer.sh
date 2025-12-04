#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"

echo "Scanning for references to 'dating_app_database/db_visualizer' or 'db_visualizer' ..."
if grep -RIn "dating_app_database/db_visualizer\|db_visualizer" -n "${ROOT_DIR}" >/dev/null; then
  echo "Found references to db_visualizer. Please remove or update them."
  grep -RIn "dating_app_database/db_visualizer\|db_visualizer" -n "${ROOT_DIR}" || true
  exit 1
fi

echo "No db_visualizer references detected in the repository."
