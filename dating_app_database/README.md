# dating_app_database container

This container is dedicated to running PostgreSQL only for the MatchFilter Dating App.

What changed:
- Removed an accidental Node.js "db_visualizer" utility (server.js, package.json, postgres.env). This container must not run any Node processes.
- startup.sh remains responsible solely for starting and configuring PostgreSQL on port 5000 and preparing the database and user.

How to use:
- Start the container or run ./startup.sh to initialize and start Postgres.
- Connect using:
  psql postgresql://appuser:dbuser123@localhost:5000/myapp
  or
  psql -h localhost -U appuser -d myapp -p 5000

Notes:
- Any UI or API to view the database should live in a separate service/container.
- db_connection.txt contains the connection command for convenience.
