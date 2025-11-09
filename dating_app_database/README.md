# dating_app_database container

This container is dedicated to running PostgreSQL only for the MatchFilter Dating App.

What changed:
- Removed an accidental Node.js "db_visualizer" utility (server.js, package.json, postgres.env). This container must not run any Node processes.
- startup.sh is responsible solely for starting and configuring PostgreSQL on port 5001 and preparing the database and user.
- The server binds to 0.0.0.0 and a readiness probe (pg_isready) confirms availability.

How to use:
- Start the container or run ./startup.sh to initialize and start Postgres.
- Connect using:
  psql postgresql://appuser:dbuser123@localhost:5001/myapp
  or
  psql -h localhost -U appuser -d myapp -p 5001

Readiness:
- The script waits until pg_isready succeeds for dbname=myapp user=appuser host=127.0.0.1 port=5001, then prints "PostgreSQL ready."

Notes:
- Any UI or API to view the database should live in a separate service/container.
- db_connection.txt contains the connection command for convenience.
- Environment variables honored:
  POSTGRES_DB=myapp
  POSTGRES_USER=appuser
  POSTGRES_PASSWORD=dbuser123
  POSTGRES_PORT=5001
