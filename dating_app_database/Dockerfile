# syntax=docker/dockerfile:1

# Use official Postgres as base
FROM postgres:15

# Set environment defaults that can be overridden at runtime
ENV POSTGRES_DB=myapp \
    POSTGRES_USER=appuser \
    POSTGRES_PASSWORD=dbuser123 \
    POSTGRES_PORT=5001

# Working directory for database container assets
# Note: We intentionally use /opt/dating_app_database and do not reference any 'db_visualizer' subdirectory.
# All scripts are copied into this directory and invoked from docker-entrypoint.sh.
WORKDIR /opt/dating_app_database

# Copy only what we need
# - startup.sh controls DB init and run
# - database_backup.sql is optional for future restore/tests; not executed by default
# - scripts for backup/restore for convenience inside container
COPY startup.sh ./startup.sh
COPY backup_db.sh ./backup_db.sh
COPY restore_db.sh ./restore_db.sh
COPY database_backup.sql ./database_backup.sql

# Ensure scripts are executable
RUN chmod +x ./startup.sh ./backup_db.sh ./restore_db.sh

# Create a minimal entrypoint wrapper to run startup.sh
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose the configured port
EXPOSE 5001

# Use our entrypoint that starts Postgres via startup.sh and keeps container running
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
