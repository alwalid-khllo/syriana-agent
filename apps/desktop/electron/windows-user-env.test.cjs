const assert = require('node:assert/strict')
const { test } = require('node:test')

const { expandWindowsEnvRefs, parseRegQueryValue, readWindowsUserEnvVar } = require('./windows-user-env.cjs')

// ── parseRegQueryValue ─────────────────────────────────────────────────────

test('parseRegQueryValue extracts a REG_SZ value', () => {
  const out = ['', 'HKEY_CURRENT_USER\\Environment', '    SYRIANA_HOME    REG_SZ    F:\\Syriana\\data', ''].join('\r\n')
  assert.equal(parseRegQueryValue(out, 'SYRIANA_HOME'), 'F:\\Syriana\\data')
})

test('parseRegQueryValue matches the name case-insensitively', () => {
  const out = 'HKEY_CURRENT_USER\\Environment\r\n    Syriana_Home    REG_EXPAND_SZ    %USERPROFILE%\\h\r\n'
  assert.equal(parseRegQueryValue(out, 'SYRIANA_HOME'), '%USERPROFILE%\\h')
})

test('parseRegQueryValue preserves spaces inside the value', () => {
  const out = '    SYRIANA_HOME    REG_SZ    C:\\Program Files\\Syriana\r\n'
  assert.equal(parseRegQueryValue(out, 'SYRIANA_HOME'), 'C:\\Program Files\\Syriana')
})

test('parseRegQueryValue returns null when the value line is absent', () => {
  const out = 'HKEY_CURRENT_USER\\Environment\r\n    Path    REG_SZ    C:\\x\r\n'
  assert.equal(parseRegQueryValue(out, 'SYRIANA_HOME'), null)
  assert.equal(parseRegQueryValue('', 'SYRIANA_HOME'), null)
  assert.equal(parseRegQueryValue('garbage', 'SYRIANA_HOME'), null)
})

// ── expandWindowsEnvRefs ───────────────────────────────────────────────────

test('expandWindowsEnvRefs expands %VAR% case-insensitively', () => {
  assert.equal(expandWindowsEnvRefs('%UserProfile%\\h', { USERPROFILE: 'C:\\Users\\jeff' }), 'C:\\Users\\jeff\\h')
})

test('expandWindowsEnvRefs leaves literal paths and unknown refs intact', () => {
  assert.equal(expandWindowsEnvRefs('F:\\Syriana\\data', {}), 'F:\\Syriana\\data')
  assert.equal(expandWindowsEnvRefs('%NOPE%\\x', {}), '%NOPE%\\x')
})

// ── readWindowsUserEnvVar ──────────────────────────────────────────────────

test('readWindowsUserEnvVar returns null off Windows without spawning', () => {
  let spawned = false
  const exec = () => {
    spawned = true
    return ''
  }
  assert.equal(readWindowsUserEnvVar('SYRIANA_HOME', { platform: 'linux', exec }), null)
  assert.equal(spawned, false)
})

test('readWindowsUserEnvVar queries HKCU\\Environment and expands the value', () => {
  const calls = []
  const exec = (cmd, args) => {
    calls.push([cmd, args])
    return 'HKEY_CURRENT_USER\\Environment\r\n    SYRIANA_HOME    REG_EXPAND_SZ    %DRIVE%\\Syriana\r\n'
  }
  const value = readWindowsUserEnvVar('SYRIANA_HOME', {
    platform: 'win32',
    env: { DRIVE: 'F:' },
    exec
  })
  assert.equal(value, 'F:\\Syriana')
  assert.deepEqual(calls, [['reg', ['query', 'HKCU\\Environment', '/v', 'SYRIANA_HOME']]])
})

test('readWindowsUserEnvVar returns null when reg exits non-zero (value missing)', () => {
  const exec = () => {
    throw new Error('reg exited 1')
  }
  assert.equal(readWindowsUserEnvVar('SYRIANA_HOME', { platform: 'win32', exec }), null)
})

test('readWindowsUserEnvVar returns null for an empty value', () => {
  const exec = () => '    SYRIANA_HOME    REG_SZ    \r\n'
  assert.equal(readWindowsUserEnvVar('SYRIANA_HOME', { platform: 'win32', exec }), null)
})
