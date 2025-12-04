# dating_app_database container

This container is dedicated to running PostgreSQL only for the MatchFilter Dating App.

What this container does:
- Runs PostgreSQL only; no Node processes or extra utilities.
- startup.sh is responsible solely for starting and configuring PostgreSQL on port 5001 and preparing the database and user.
- The server binds to 0.0.0.0 and a readiness probe (pg_isready) confirms availability.

How to build and run (Docker):
1) Build the image
   docker build -t dating_app_database:latest .

2) Run the container
   docker run --name dating_app_db --rm -p 5001:5001 \
     -e POSTGRES_DB=myapp \
     -e POSTGRES_USER=appuser \
     -e POSTGRES_PASSWORD=dbuser123 \
     -e POSTGRES_PORT=5001 \
     dating_app_database:latest

3) Connect using:
   psql postgresql://appuser:dbuser123@localhost:5001/myapp
   or
   psql -h localhost -U appuser -d myapp -p 5001

How to use without Docker:
- Start locally or run ./startup.sh to initialize and start Postgres.
- Connection string is the same as above.

Readiness:
- The script waits until pg_isready succeeds for dbname=myapp user=appuser host=127.0.0.1 port=5001, then prints "PostgreSQL ready.".

Notes:
- Any UI or API to view the database should live in a separate service/container.
- db_connection.txt contains the connection command for convenience.
- Environment variables honored:
  POSTGRES_DB=myapp
  POSTGRES_USER=appuser
  POSTGRES_PASSWORD=dbuser123
  POSTGRES_PORT=5001
