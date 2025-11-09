'use strict';

const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const { getClient } = require('./helpers/dbClient');

let client;

const expectedPublicTables = new Set([
  'auth_group',
  'auth_group_permissions',
  'auth_permission',
  'auth_user',
  'auth_user_groups',
  'auth_user_user_permissions',
  'authtoken_token',
  'core_filterpreset',
  'core_match',
  'core_message',
  'core_profile',
  'django_admin_log',
  'django_content_type',
  'django_migrations',
  'django_session'
]);

before(async () => {
  client = getClient();
  await client.connect();
});

after(async () => {
  if (client) await client.end();
});

test('public schema exists', async () => {
  const res = await client.query(`
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name = 'public'
  `);
  assert.equal(res.rowCount, 1, 'public schema should exist');
});

test('expected tables exist in public schema', async () => {
  const res = await client.query(`
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
  `);
  const existing = new Set(res.rows.map(r => r.table_name));
  // For each expected table, assert existence
  for (const t of expectedPublicTables) {
    assert.ok(existing.has(t), `Expected table "${t}" to exist in schema "public"`);
  }
});
