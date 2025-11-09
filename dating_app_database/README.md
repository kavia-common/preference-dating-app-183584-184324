# dating_app_database container

This container is dedicated to running PostgreSQL only for the MatchFilter Dating App.

What changed:
- Removed an accidental Node.js "db_visualizer" utility (e.g., server.js, package.json, postgres.env). This container must not run any Node processes.
- startup.sh is responsible solely for starting and configuring PostgreSQL on port 5001 and preparing the database and user.
- The server binds to 0.0.0.0 and a readiness probe (pg_isready) confirms availability.
- No db_visualizer folder or Node-related files are created during startup.
- A Dockerfile and docker-compose.yml are provided and contain no references to any "db_visualizer" directory.
- CI/build/startup scripts must not attempt to `cd` into `dating_app_database/db_visualizer`. The correct path for all operations is simply `dating_app_database` (e.g., `docker build -t dating_app_database ./dating_app_database`).

How to use (local script):
- Run ./startup.sh to initialize and start Postgres.
- Connect using:
  psql postgresql://appuser:dbuser123@localhost:5001/myapp
  or
  psql -h localhost -U appuser -d myapp -p 5001

How to use with Docker:
- From the repository root:
  docker compose up --build dating_app_database
- Or directly:
  docker build -t dating_app_database ./dating_app_database
  docker run --rm -p 5001:5001 --name dating_app_database \
    -e POSTGRES_DB=myapp -e POSTGRES_USER=appuser -e POSTGRES_PASSWORD=dbuser123 -e POSTGRES_PORT=5001 \
    dating_app_database

Readiness:
- startup.sh waits until pg_isready succeeds for dbname=myapp user=appuser host=127.0.0.1 port=5001, then prints "PostgreSQL ready." and exits 0.

Notes:
- Any UI or API to view the database should live in a separate service/container.
- db_connection.txt contains the connection command for convenience.
- Environment variables honored:
  POSTGRES_DB=myapp
  POSTGRES_USER=appuser
  POSTGRES_PASSWORD=dbuser123
  POSTGRES_PORT=5001
