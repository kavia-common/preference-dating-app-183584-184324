# Dating App Database

This directory contains the PostgreSQL database resources for the Preference Dating App.
All scripts and Dockerfiles use the WORKDIR `/opt/dating_app_database`. There is no `db_visualizer` subdirectory.

Verification of db_visualizer removal:
- No references to `db_visualizer` remain anywhere in the build or startup paths.
- A repository-wide search confirms there are no remaining references to `db_visualizer`, nor any commands attempting to `cd` into `dating_app_database/db_visualizer` in the Dockerfile, entrypoint, startup scripts, CI/build scripts, hidden configs, or any RUN/CMD statements.
- Scripts and Dockerfile use WORKDIR `/opt/dating_app_database` and do not assume any nested directories like `db_visualizer`.

Where could a stray "cd dating_app_database/db_visualizer" come from?
- External preview/build system configurations sometimes hardcode a subdirectory name.
- If any such config tries to "cd preference-dating-app-183584-184324/dating_app_database/db_visualizer" or similar, update it to:
  - Repo path: preference-dating-app-183584-184324/dating_app_database
  - Container WORKDIR: /opt/dating_app_database

Quick check script:
- Run the following from repo root to ensure nothing in-repo still references db_visualizer:
  grep -RIn "dating_app_database/db_visualizer\|db_visualizer" -n || true

