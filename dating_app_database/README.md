# Dating App Database (PostgreSQL)

This container is dedicated to running PostgreSQL only for the Preference/MatchFilter Dating App.

What this container does:
- Runs PostgreSQL only; no Node processes or extra utilities.
- `startup.sh` starts and configures PostgreSQL on port `5001`, ensures role/database, sets permissions, and writes a convenience `db_connection.txt`.
- The server binds to `0.0.0.0`, and a readiness probe (`pg_isready`) confirms availability before proceeding.

Security/Access:
- Default credentials can be overridden via environment variables.
- Host connections require md5 authentication (configured in `pg_hba.conf` at init).

Environment variables (defaults):
- POSTGRES_DB=myapp
- POSTGRES_USER=appuser
- POSTGRES_PASSWORD=dbuser123
- POSTGRES_PORT=5001

Build and run (Docker):
1) Build the image
   docker build -t dating_app_database:latest .

2) Run the container
   docker run --name dating_app_db --rm -p 5001:5001 \
     -e POSTGRES_DB=myapp \
     -e POSTGRES_USER=appuser \
     -e POSTGRES_PASSWORD=dbuser123 \
     -e POSTGRES_PORT=5001 \
     dating_app_database:latest

3) Verify from host (psql required)
   psql postgresql://appuser:dbuser123@localhost:5001/myapp -c "SELECT now();"

Connect manually:
- psql postgresql://appuser:dbuser123@localhost:5001/myapp
  or
- psql -h localhost -U appuser -d myapp -p 5001

Using without Docker:
- You can run `./startup.sh` locally to initialize/start Postgres (requires appropriate permissions/binaries).
- The script writes a connection helper to `db_connection.txt`.

Readiness:
- The script waits until `pg_isready` succeeds for host=127.0.0.1 dbname=${POSTGRES_DB} user=${POSTGRES_USER} port=${POSTGRES_PORT} and then prints "PostgreSQL ready.".

Notes:
- Any UI or API to view the database should live in a separate service/container.
- `db_connection.txt` contains a ready-to-use `psql` command for convenience.

Verification of db_visualizer removal:
- A repository-wide search confirms there are no remaining references to `db_visualizer`, nor any commands attempting to `cd` into `dating_app_database/db_visualizer` in the Dockerfile, entrypoint, startup scripts, CI/build scripts, or any RUN/CMD statements.
- This ensures the image build and startup do not depend on any missing `db_visualizer` directory or tools.
