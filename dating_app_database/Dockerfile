# syntax=docker/dockerfile:1

# Use official postgres base image for compatibility
FROM postgres:16

# Set environment defaults (can be overridden)
ENV POSTGRES_DB=myapp \
    POSTGRES_USER=appuser \
    POSTGRES_PASSWORD=dbuser123 \
    POSTGRES_PORT=5001

# Workdir for our custom scripts and data
WORKDIR /app

# Copy startup script and helper files
COPY startup.sh /app/startup.sh
COPY db_connection.txt /app/db_connection.txt
COPY database_backup.sql /app/database_backup.sql
COPY restore_db.sh /app/restore_db.sh
COPY backup_db.sh /app/backup_db.sh

# Ensure scripts are executable
RUN chmod +x /app/startup.sh /app/restore_db.sh /app/backup_db.sh

# Expose custom Postgres port
EXPOSE 5001

# Note: We use our startup.sh (which internally starts postgres on port 5001)
# to avoid relying on any previous db_visualizer or Node processes.
ENTRYPOINT ["/bin/bash", "/app/startup.sh"]
