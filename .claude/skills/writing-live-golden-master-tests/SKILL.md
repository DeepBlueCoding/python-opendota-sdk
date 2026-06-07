---
name: writing-live-golden-master-tests
description: >-
  Writes or fixes pytest tests for the python-opendota-sdk that hit the REAL
  OpenDota API and assert stable golden values that won't rot. Use whenever the
  user wants a test for an endpoint, a golden master test, to assert
  match/player/hero/team data, or when a live test is failing/flaky, a hero count
  changed for a new patch, or a test broke because a display name changed. Every
  test in tests/ calls the live API (NO pytest-httpx mocking despite CLAUDE.md and
  AGENTS.md claiming it). Encodes which values are safe to golden-master, the
  account_id-not-personaname lesson, and how to run focused without spamming the
  rate-limited API.
allowed-tools: Read, Edit, Write, Grep, Bash(uv run pytest*)
---

# Write a live golden-master test

**Every test in `tests/` hits the LIVE OpenDota API.** There is NO pytest-httpx /
`httpx_mock` wiring — `CLAUDE.md` and `AGENTS.md` claim pytest-httpx mocking, but
that is aspirational and false. Tests just construct `OpenDota()` and make real,
rate-limited network calls (3s delay between calls without an API key).

## File skeleton

Mirror the existing test files exactly:
```python
"""Tests for <feature> endpoints using Golden Master approach with real data."""

import sys

import pytest

sys.path.insert(0, 'src')
from opendota.client import OpenDota


class TestFeature:
    @pytest.fixture
    async def client(self):
        async with OpenDota() as client:
            yield client

    @pytest.mark.asyncio
    async def test_<thing>_golden_master(self, client):
        result = await client.get_<thing>(...)
        assert result.<stable_field> == <known_value>
```

Conventions (from `pyproject.toml [tool.pytest.ini_options]`): `asyncio_mode =
"auto"`, files `test_*.py`, classes `Test*`, functions `test_*`. The
`sys.path.insert(0, 'src')` then `from opendota.client import OpenDota` import
shim is required and used by every test file. For dict-style assertions use a
`format='json'` client; for attribute assertions use the default pydantic client.

## What to golden-master vs what to avoid (the "why")

Commit `1ff95ce` ("assert stable IDs instead of mutable display names") is the
core lesson: OpenDota joins display names (`personaname`, curated pro names) at
read time from mutable Steam/GC state, and accounts keep playing. So:

- **Assert the stable key** (`account_id`, `match_id`, hero `id`/internal `name`)
  and, for names, only shape: `assert isinstance(x, str) and len(x) > 0`.
  **NEVER golden-master a `personaname`.** A `name` that is a fixed real name
  (e.g. `player.profile.name == "Dendi"`) is borderline-safe but the
  `personaname` next to it must only be existence-checked — see
  `tests/test_players.py` lines 31-35.
- **Never golden-master "the most recent match"** of an active account — it
  changes constantly. Assert the API *contract* instead:
  `start_times == sorted(start_times, reverse=True)` (most-recent-first ordering).
- **Safe stable goldens** (verified in-repo): completed match `8461956309` →
  `duration == 3512`, `radiant_win is False`, `radiant_score == 11`,
  `dire_score == 24`, `start_time == 1757872818`, `len(players) == 10`,
  `players[0].account_id == 898754153`, `players[0].hero_id == 8` (Juggernaut);
  hero ids/internal names (`npc_dota_hero_antimage` id `1`, `npc_dota_hero_axe`
  id `2`, `npc_dota_hero_bane` id `3` with `primary_attr == "all"`).
- **Do NOT** assert `isinstance`/`len >= 0`/field-existence as the *only* check
  on a value that has a stable known value — that defeats the golden master.
  Existence checks are only the fallback for genuinely mutable fields (names,
  leaderboard rank, computed rating).

## Patch-drifting goldens — update together

Hero counts change each Dota patch. `tests/test_heroes.py` currently expects (for
patch 7.40): `len(heroes) == 127`, `36` STR, `35` AGI, `34` INT, `22` Universal
(`"all"`), and `len(heroes) == len(hero_stats) == 127`. Git history shows
126→127 churn (commits `05130ad`, `9ff78d6`). When a new patch lands, update ALL
of these numbers in the same edit, plus any per-attribute counts, or the file
fails as a unit.

## Running tests — focused only

Every call is rate-limited; do not run the whole suite to check one test.
```bash
uv run pytest tests/test_matches.py::TestMatches::test_get_match_8461956309_golden_master
```
Coverage uses `--cov=opendota` (NOT `--cov=python_opendota` as `CLAUDE.md` says):
```bash
uv run pytest tests/test_heroes.py --cov=opendota
```
A live-test caveat: because tests hit the real API, a transient OpenDota change
can fail a run that has no code bug — confirm against the API before "fixing"
code to match.
