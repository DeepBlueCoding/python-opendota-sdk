---
name: add-api-endpoint
description: >-
  Adds a new OpenDota API endpoint to the python-opendota-sdk: client method on
  the OpenDota class, response TypeAlias, Pydantic model, dual pydantic/json
  output, and a live golden-master test. Use whenever the user wants to add a new
  endpoint, wrap an OpenDota route (e.g. /distributions, /rankings, /benchmarks,
  /scenarios, /findMatches), add a get_<something> method to the client, expose
  another API call, or support a new OpenDota route — even if they don't name this
  skill. Covers the correct package layout (opendota at src/opendota/, NOT
  python_opendota) and the self.get + _format_response + cast pattern every method
  follows.
allowed-tools: Read, Edit, Write, Grep, Bash(uv run ruff*), Bash(uv run mypy*)
---

# Add an OpenDota API endpoint

All endpoint methods live **directly on the `OpenDota` class** in
`src/opendota/client.py`. `src/opendota/endpoints/base.py` is an unused stub — do
not put endpoint logic there. The `endpoints/` package is vestigial.

The repo `CLAUDE.md` and `RELEASE.md` are stale: they say `src/python_opendota/`,
`--cov=python_opendota`, and pytest-httpx mocking. **All three are wrong.** The
real package is `opendota` at `src/opendota/`, the dist name is
`python-opendota-sdk`, coverage flag is `--cov=opendota`, and tests hit the LIVE
API with no mocking. Follow this skill, not those files, where they conflict.

## Workflow

1. **Model** — add/extend the Pydantic model in `src/opendota/models/<domain>.py`,
   then export it from `src/opendota/models/__init__.py` (both the import and the
   alphabetical `__all__` list). See `add-model-field` for field rules.
2. **TypeAlias** — declare the response alias(es) near lines 30-54 of `client.py`,
   beside the existing aliases, grouped by domain with a `# <Domain> type aliases`
   comment.
3. **Import** — add the model to the per-module imports at the top of `client.py`
   (lines 21-27), e.g. `from .models.<domain> import Foo`.
4. **Method** — write the async method on the `OpenDota` class following the exact
   pattern below.
5. **Test** — add a live golden-master test in `tests/test_<domain>.py`
   (see `writing-live-golden-master-tests`).
6. **Verify** — `uv run ruff check src/ tests/` and
   `uv run mypy src/ --ignore-missing-imports`. Do NOT run the full pytest suite
   casually; it makes rate-limited network calls. Run only the one new test.

## Exact method patterns

Single object:
```python
async def get_foo(self, foo_id: int) -> FooResponse:
    """Get foo data by ID."""
    data = await self.get(f"foos/{foo_id}")
    foo = Foo(**data)
    return cast(FooResponse, self._format_response(foo))
```

List with optional filters (build params, skip `None`):
```python
async def get_foos(self, limit: Optional[int] = None) -> FoosResponse:
    """Get foos."""
    params: Dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    data = await self.get("foos", params=params or None)
    foos = [Foo(**item) for item in data]
    return cast(FoosResponse, self._format_response(foos))
```

TypeAliases (one per shape):
```python
FooResponse: TypeAlias = Union[Foo, dict]
FoosResponse: TypeAlias = Union[List[Foo], List[dict]]
```

## Rules (the "why")

- **`self.get()` defaults `use_cache=True`** and caches GETs to `~/dota2/cache`.
  Pass `use_cache=False` for volatile or POST endpoints — `get_pro_matches` and
  `request_match` already do this. Caching a live-changing endpoint serves stale
  data; cache it only if the resource is effectively immutable (a finished match,
  hero metadata).
- **POST endpoints** call `await self._request("POST", ...)` directly (see
  `request_match` lines 412-428), not `self.get()`, and always `use_cache=False`.
- **Never call `model_dump()` yourself.** `_format_response` (lines 240-254) does
  the pydantic→dict conversion only when `self.format == 'json'`; pydantic is the
  default. Always return `cast(..., self._format_response(model))`.
- **`params or None`** — pass an empty dict as `None` so it isn't sent as empty
  query string (see `get_team_matches`, `get_league_matches`).
- **Build params explicitly**: `params: Dict[str, Any] = {}` then
  `if x is not None: params["x"] = x`. Never pass `None` values through; OpenDota
  treats a literal `None` differently from an omitted param.
- **Plain-dict endpoints exist**: `get_parsed_matches` and `get_league_matches`
  return `List[Dict[str, Any]]` directly without a model. Only do this when no
  model is warranted; prefer a typed model.

## Nested / renamed API keys

If the API wraps or renames keys, add a `from_api_response` classmethod on the
model and call it in the method — do not munge dicts inline. Example: the parse
endpoint returns `{"job": {"jobId": N}}`; `ParseJobRequest.from_api_response`
(in `models/parse_job.py`) unwraps it, and `get_parse_job_status` remaps `jobId`
→ `job_id` at construction. Mirror that style.

## Checklist before done

- [ ] Model exported from `models/__init__.py` import block AND `__all__` (alphabetical)
- [ ] Model imported at top of `client.py`
- [ ] TypeAlias(es) declared near other aliases
- [ ] Method uses `self.get(...)` (or `self._request("POST", ...)`) + `cast(..., self._format_response(...))`
- [ ] `use_cache=False` if the endpoint is volatile or POST
- [ ] One live golden-master test added
- [ ] `uv run ruff check src/ tests/` clean
- [ ] `uv run mypy src/ --ignore-missing-imports` clean
