#!/bin/bash
set -euo pipefail

# Universal Database Restore Script
# Automatically detects backup type and restores to running database
# Behavior:
# - For PostgreSQL: restore as postgres superuser, target port ${DB_PORT:-5001}, fail-fast with ON_ERROR_STOP=1
# - Do NOT suppress stderr; print clear success/failure messages

DB_NAME="myapp"
DB_USER="appuser"
DB_PASSWORD="dbuser123"
DB_PORT="${DB_PORT:-5001}"

# SQLite restore
if [ -f "database_backup.db" ]; then
    echo "Restoring SQLite database from backup..."
    cp "database_backup.db" "${DB_NAME}"
    echo "✓ Database restored successfully (SQLite)"
    exit 0
fi

# PostgreSQL/MySQL restore from SQL file
if [ -f "database_backup.sql" ]; then
    # Try PostgreSQL first
    PG_VERSION=$(ls /usr/lib/postgresql/ 2>/dev/null | head -1 || true)
    if [ -n "${PG_VERSION:-}" ]; then
        PG_BIN="/usr/lib/postgresql/${PG_VERSION}/bin"
        # Check readiness on the configured port (default 5001)
        if sudo -u postgres "${PG_BIN}/pg_isready" -h localhost -p "${DB_PORT}" >/dev/null 2>&1; then
            echo "Restoring PostgreSQL database from backup as superuser on port ${DB_PORT} ..."
            # Run restore into 'postgres' so dump can DROP/CREATE myapp and \connect
            if sudo -u postgres "${PG_BIN}/psql" -h localhost -p "${DB_PORT}" -d postgres -v ON_ERROR_STOP=1 < database_backup.sql; then
                echo "✓ PostgreSQL database restored successfully."
                exit 0
            else
                code=$?
                echo "✗ PostgreSQL restore failed with exit code ${code}."
                exit "${code}"
            fi
        fi
    fi

    # Try MySQL - Do not specify a database because the dump may contain CREATE DATABASE
    if mysqladmin ping -h localhost -P "${DB_PORT}" --silent 2>/dev/null || \
       sudo mysqladmin ping --socket=/var/run/mysqld/mysqld.sock --silent 2>/dev/null; then
        echo "Restoring MySQL database from backup..."
        if mysql -h localhost -P "${DB_PORT}" -u "${DB_USER}" -p"${DB_PASSWORD}" -e "SELECT 1" >/dev/null 2>&1; then
            if mysql -h localhost -P "${DB_PORT}" -u "${DB_USER}" -p"${DB_PASSWORD}" < database_backup.sql; then
                echo "✓ Database restored successfully (MySQL via TCP port ${DB_PORT})"
                exit 0
            else
                code=$?
                echo "✗ MySQL restore failed with exit code ${code} (TCP as ${DB_USER})."
                exit "${code}"
            fi
        fi

        if mysql -h localhost -P "${DB_PORT}" -u root -p"${DB_PASSWORD}" -e "SELECT 1" >/dev/null 2>&1; then
            if mysql -h localhost -P "${DB_PORT}" -u root -p"${DB_PASSWORD}" < database_backup.sql; then
                echo "✓ Database restored successfully (MySQL via TCP port ${DB_PORT} as root)"
                exit 0
            else
                code=$?
                echo "✗ MySQL restore failed with exit code ${code} (TCP as root)."
                exit "${code}"
            fi
        fi

        if sudo mysql --socket=/var/run/mysqld/mysqld.sock -u root -p"${DB_PASSWORD}" -e "SELECT 1" >/dev/null 2>&1; then
            if sudo mysql --socket=/var/run/mysqld/mysqld.sock -u root -p"${DB_PASSWORD}" < database_backup.sql; then
                echo "✓ Database restored successfully (MySQL via socket)"
                exit 0
            else
                code=$?
                echo "✗ MySQL restore failed with exit code ${code} (socket as root)."
                exit "${code}"
            fi
        fi

        if sudo mysql --socket=/var/run/mysqld/mysqld.sock -u root -e "SELECT 1" >/dev/null 2>&1; then
            if sudo mysql --socket=/var/run/mysqld/mysqld.sock -u root < database_backup.sql; then
                echo "✓ Database restored successfully (MySQL via socket, no password)"
                exit 0
            else
                code=$?
                echo "✗ MySQL restore failed with exit code ${code} (socket as root, no password)."
                exit "${code}"
            fi
        fi

        echo "⚠ MySQL is running but authentication failed"
        echo "  Please check your credentials"
        exit 1
    fi
fi

# MongoDB restore from archive
if [ -f "database_backup.archive" ]; then
    if mongosh --port "${DB_PORT}" --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
        echo "Restoring MongoDB database from backup..."
        # Create database if it doesn't exist
        mongosh --port "${DB_PORT}" --eval "use ${DB_NAME}" > /dev/null 2>&1
        if mongorestore --port "${DB_PORT}" --archive=database_backup.archive --drop --quiet; then
            echo "✓ Database restored successfully (MongoDB)"
            exit 0
        else
            code=$?
            echo "✗ MongoDB restore failed with exit code ${code}."
            exit "${code}"
        fi
    fi
fi

echo "ℹ No backup found or database not running"
echo "  Starting with fresh database"
echo ""
echo "Backup files checked:"
echo "  - database_backup.db (SQLite)"
echo "  - database_backup.sql (PostgreSQL/MySQL)"
echo "  - database_backup.archive (MongoDB)"
exit 0
