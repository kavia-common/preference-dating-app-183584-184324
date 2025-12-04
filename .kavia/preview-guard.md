This project does not contain a 'db_visualizer' directory under dating_app_database.
If an external preview/build system attempts 'cd dating_app_database/db_visualizer', update its config to point to:
- Repo path: preference-dating-app-183584-184324/dating_app_database
- Container WORKDIR: /opt/dating_app_database

Inside the database container, scripts run from WORKDIR /opt/dating_app_database. There is no nested db_visualizer path.

To verify there are no in-repo references, run:
  grep -RIn "dating_app_database/db_visualizer\|db_visualizer" -n || true
