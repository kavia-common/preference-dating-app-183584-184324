# dating_app_database – PostgreSQL Test Suite

This is a lightweight Node.js test suite (Node 18+ using node:test) that validates:
- Connectivity to the running PostgreSQL instance
- Presence of expected schemas/tables
- Basic CRUD operations on a representative table

It reads environment variables to connect to the DB. Defaults are aligned with the container startup script (port 5001).

## Prerequisites

- Node.js v18 or later
- A running PostgreSQL instance (the container's startup.sh starts one on port 5001)
- The database should be reachable locally

## Environment variables

Create a .env file in this folder (tests) or at repository root with the following variables:

Copy from .env.example:
```
cp .env.example .env
```

Variables:
- PGHOST (default localhost)
- PGPORT (default 5001)
- PGDATABASE (default myapp)
- PGUSER (default appuser)
- PGPASSWORD (default dbuser123)

Alternatively, use:
- DATABASE_URL=postgresql://appuser:dbuser123@localhost:5001/myapp

The DATABASE_URL, if present, overrides the discrete vars.

## Install and Run

From this tests directory:

```
npm install
npm test
```

CI mode (TAP output):
```
npm run test:ci
```

These commands are non-interactive and work directly via CLI.

## Notes

- Tests use transactions for CRUD and rollback to keep the DB clean.
- Expected tables are derived from the included database_backup.sql.
- If the DB is not yet initialized, run the container's startup script first.
