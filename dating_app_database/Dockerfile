# syntax=docker/dockerfile:1

FROM postgres:15-alpine

# Use a fixed working directory; do not cd into any subdirectories like 'db_visualizer'
WORKDIR /opt/dating_app_database

COPY . /opt/dating_app_database

# Use a minimal entrypoint that respects the WORKDIR
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["postgres"]
