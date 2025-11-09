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
  if (client) await client.end();
});

test('CRUD on public.core_filterpreset within transaction', async (t) => {
  // Run in a transaction so we can rollback and keep DB clean
  await client.query('BEGIN');

  try {
    // Create: insert a row
    const insertRes = await client.query(
      `
      INSERT INTO public.core_filterpreset
        (created_at, updated_at, name, min_height_cm, max_height_cm, min_weight_kg, max_weight_kg, genders, is_public, owner_id)
      VALUES
        (NOW(), NOW(), $1, $2, $3, $4, $5, $6::jsonb, $7, $8)
      RETURNING id, name, min_height_cm, max_height_cm, genders, is_public
      `,
      ['Test Preset A', 150, 200, 50, 100, JSON.stringify(['male', 'female']), true, null]
    );
    assert.equal(insertRes.rowCount, 1, 'one row should be inserted');
    const newId = insertRes.rows[0].id;
    assert.ok(newId, 'insert should return an id');

    // Read
    const readRes = await client.query(
      'SELECT id, name, min_height_cm, max_height_cm, genders, is_public FROM public.core_filterpreset WHERE id = $1',
      [newId]
    );
    assert.equal(readRes.rowCount, 1, 'inserted row should be readable');
    assert.equal(readRes.rows[0].name, 'Test Preset A');

    // Update
    const updateRes = await client.query(
      'UPDATE public.core_filterpreset SET name = $1, updated_at = NOW() WHERE id = $2',
      ['Test Preset A - Updated', newId]
    );
    assert.equal(updateRes.rowCount, 1, 'one row should be updated');

    const readUpdated = await client.query(
      'SELECT name FROM public.core_filterpreset WHERE id = $1',
      [newId]
    );
    assert.equal(readUpdated.rows[0].name, 'Test Preset A - Updated');

    // Delete
    const deleteRes = await client.query(
      'DELETE FROM public.core_filterpreset WHERE id = $1',
      [newId]
    );
    assert.equal(deleteRes.rowCount, 1, 'one row should be deleted');

    const readDeleted = await client.query(
      'SELECT id FROM public.core_filterpreset WHERE id = $1',
      [newId]
    );
    assert.equal(readDeleted.rowCount, 0, 'row should be deleted');

  } finally {
    // Always rollback to keep DB pristine
    await client.query('ROLLBACK');
  }
});
