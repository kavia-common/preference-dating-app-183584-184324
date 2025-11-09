'use strict';

/**
 * Utility to create a pg client based on env variables.
 * Reads DATABASE_URL if provided, otherwise uses discrete PG* variables.
 * Loads .env from the tests directory if present.
 */
const path = require('path');
const fs = require('fs');
const dotenv = require('dotenv');
const { Client } = require('pg');

// Load .env from tests directory if it exists
const envPath = path.join(__dirname, '..', '..', '.env');
const envExamplePath = path.join(__dirname, '..', '..', '.env.example');
if (fs.existsSync(envPath)) {
  dotenv.config({ path: envPath });
} else {
  // fallback: try root of repository, otherwise rely on process env
  const rootEnv = path.join(__dirname, '..', '..', '..', '.env');
  if (fs.existsSync(rootEnv)) {
    dotenv.config({ path: rootEnv });
  }
}

// Build connection config
function buildConfig() {
  const fromUrl = process.env.DATABASE_URL || process.env.POSTGRES_URL;
  if (fromUrl) {
    return { connectionString: fromUrl, application_name: 'db-tests' };
  }
  const host = process.env.PGHOST || 'localhost';
  const port = Number(process.env.PGPORT || process.env.POSTGRES_PORT || 5001);
  const database = process.env.PGDATABASE || process.env.POSTGRES_DB || 'myapp';
  const user = process.env.PGUSER || process.env.POSTGRES_USER || 'appuser';
  const password = process.env.PGPASSWORD || process.env.POSTGRES_PASSWORD || 'dbuser123';
  return {
    host,
    port,
    database,
    user,
    password,
    application_name: 'db-tests'
  };
}

// PUBLIC_INTERFACE
function getClient() {
  /** Create a new pg Client using environment configuration. */
  const config = buildConfig();
  return new Client(config);
}

module.exports = {
  // PUBLIC_INTERFACE
  getClient
};
