---
name: add-model-field
description: >-
  Adds or updates fields on the python-opendota-sdk Pydantic v2 response models
  (Match, Player, Hero, HeroStats, PlayerProfile, ProMatch, Team, League, etc.)
  when the OpenDota API adds data or for a new Dota patch, without breaking parsing
  of older or partial responses. Use whenever the user wants to add a field to a
  model, says OpenDota added a new field, update models for a new patch, fix a
  model that drops a field the API returns, or hits a missing-attribute / KeyError
  / ValidationError on a model. Encodes the Optional-by-default house rule and the
  @property convenience and from_api_response adapter patterns.
allowed-tools: Read, Edit, Grep
---

# Add or update a Pydantic model field

Models are Pydantic v2 `BaseModel` in `src/opendota/models/<domain>.py`
(`match.py`, `hero.py`, `player.py`, `team.py`, `league.py`, `pro_player.py`,
`parse_job.py`).

## Workflow

1. Locate the model in `src/opendota/models/<domain>.py`.
2. Add the field as `Optional[Type] = None` under the matching section comment
   (e.g. `# Combat stats`, `# Ward placement` in `match.py`).
3. If a derived value is needed, add an `@property`, not a stored field.
4. If the new model itself is new, export it from `models/__init__.py` (import +
   alphabetical `__all__`).
5. Update or add the matching live golden-master assertion in `tests/test_<domain>.py`
   (see `writing-live-golden-master-tests`), and the docs snippet in
   `docs/api/models.md` if the field is notable.

## Rules (the "why")

- **New fields MUST be `Optional[...] = None`.** OpenDota omits keys constantly
  (partial/unparsed matches, anonymized players). A non-Optional field raises
  `ValidationError` the moment the key is missing, breaking otherwise-fine parses.
  `match.Player` has ~135 Optional fields for exactly this reason.
- **Required (non-Optional) fields exist only where the API always returns them.**
  Current examples: `Match.match_id/duration/radiant_win/players/game_mode/
  lobby_type/start_time/radiant_score/dire_score`, `PublicMatch.match_seq_num`,
  `PlayerMatch.match_id/leaver_status`. Adding a new required field is a
  regression risk — default to Optional unless you have proof the key is always
  present.
- **Field names match the raw API JSON exactly** — `isRadiant`, `leagueid`,
  `personaname` stay camelCase/lowercase as the API sends them. Do NOT snake_case
  a real API key; Pydantic would then silently drop the data (no alias = no match).
- **For a JSON key that isn't a valid Python identifier**, use
  `Field(None, alias="...")`. See `HeroStats` bracket stats:
  `field_1_pick: Optional[int] = Field(None, alias="1_pick")`.
- **Convenience/derived values use `@property`, never stored fields.** Pattern,
  present on `Match`, `PublicMatch`, `ProMatch`, `PlayerMatch`:
  ```python
  @property
  def start_datetime(self) -> datetime:
      return datetime.fromtimestamp(self.start_time)
  ```
  `PlayerProfile.last_login_datetime` shows the nullable variant returning
  `Optional[datetime]`.
- **Nested / renamed keys → adapter, not inline munging.** Add a
  `from_api_response` classmethod (see `ParseJobRequest.from_api_response`
  unwrapping `{"job": {"jobId": N}}`) or remap at construction (see
  `get_parse_job_status` doing `ParseJob(job_id=data["jobId"], ...)`). Keep the
  client method thin.

## Examples

Add a combat stat to `match.Player` (under `# Combat stats`):
```python
roshan_kills: Optional[int] = None
```

Add a bracketed stat to `HeroStats` (under the bracket section):
```python
field_9_pick: Optional[int] = Field(None, alias="9_pick")
```

Add a derived convenience to a model that has a unix `end_time`:
```python
@property
def end_datetime(self) -> datetime:
    return datetime.fromtimestamp(self.end_time)
```
