'use strict';

const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const { getClient } = require('./helpers/dbClient');

let client;

before(async () => {
  client = getClient();
  await client.connect();
});

after(async () => {
  if (client) {
    await client.end();
  }
});

test('can connect to PostgreSQL and select version()', async () => {
  const res = await client.query('SELECT version() as v');
  assert.ok(res.rows.length === 1, 'Expected 1 row from version()');
  assert.match(res.rows[0].v, /PostgreSQL/i);
});

test('reports current database and user', async () => {
  const res = await client.query('SELECT current_database() as db, current_user as usr');
  assert.equal(res.rows[0].db, process.env.PGDATABASE || process.env.POSTGRES_DB || 'myapp');
  assert.equal(res.rows[0].usr, process.env.PGUSER || process.env.POSTGRES_USER || 'appuser');
});
