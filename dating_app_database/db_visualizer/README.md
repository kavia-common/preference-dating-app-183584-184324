# Placeholder: db_visualizer (Do Not Use)

This directory exists only as a defensive placeholder to prevent external build/preview systems from failing when they attempt to execute:
  cd dating_app_database/db_visualizer

There is no database visualizer component in this repository. All database scripts and Dockerfiles operate from the WORKDIR:
  /opt/dating_app_database

Instructions:
- Do not add code here. Do not reference this path in any scripts.
- If you control the build/preview config that tries to enter this directory, update it to use the correct working directory:
  - In container: WORKDIR /opt/dating_app_database
  - In repo: preference-dating-app-183584-184324/dating_app_database

For CI and maintainers:
- This directory is a no-op and safe to keep. It prevents failures from external scripts we cannot modify.
- If you remove this placeholder, ensure the upstream configuration no longer issues 'cd dating_app_database/db_visualizer'.

