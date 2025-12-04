# Dating App Database Container

This container builds and runs a PostgreSQL instance for the Preference Dating App.

Key points:
- Base image: postgres:15
- Exposed port: 5001 (overridable via POSTGRES_PORT)
- WORKDIR: /opt/dating_app_database
- Startup flow: docker-entrypoint.sh -> startup.sh (which launches postgres in background and performs idempotent init)

Verification of db_visualizer removal:
- No references to `db_visualizer` remain anywhere in the build or startup paths.
- A repository-wide search confirms there are no remaining references to `db_visualizer`, nor any commands attempting to `cd` into `dating_app_database/db_visualizer` in the Dockerfile, entrypoint, startup scripts, CI/build scripts, or any RUN/CMD statements.
- Scripts and Dockerfile use WORKDIR `/opt/dating_app_database` and do not assume any nested directories like `db_visualizer`.

Build and run:

1) Build the image (from repository root or this directory):
   docker build -t dating_app_database:latest preference-dating-app-183584-184324/dating_app_database

2) Run the container:
   docker run --name dating-db -p 5001:5001 \
     -e POSTGRES_DB=myapp \
     -e POSTGRES_USER=appuser \
     -e POSTGRES_PASSWORD=dbuser123 \
     dating_app_database:latest

Environment variables:
- POSTGRES_DB (default: myapp)
- POSTGRES_USER (default: appuser)
- POSTGRES_PASSWORD (default: dbuser123)
- POSTGRES_PORT (default: 5001)

Notes:
- startup.sh ensures PGDATA initialization, creates/updates the role and database, and makes Postgres listen on 0.0.0.0:${POSTGRES_PORT}.
- docker-entrypoint.sh does not `cd` into any removed directories; it relies on WORKDIR `/opt/dating_app_database`.
- If you mount a volume to /var/lib/postgresql/data, ensure permissions allow postgres to write (handled best by Docker volume defaults).

Troubleshooting:
- To verify readiness: psql postgresql://appuser:dbuser123@localhost:5001/myapp
- To view logs: docker logs -f dating-db
