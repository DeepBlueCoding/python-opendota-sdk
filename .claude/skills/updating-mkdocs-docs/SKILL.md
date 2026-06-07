---
name: updating-mkdocs-docs
description: >-
  Writes or fixes the python-opendota-sdk mkdocs-material documentation and keeps
  the hand-written API reference pages in sync with the actual code in
  src/opendota/client.py. Use whenever the user wants to update the docs, document
  a new endpoint, fix the API reference, write a getting-started or examples
  snippet, or says the docs are out of date / show a wrong signature. Flags the
  known get_match() signature drift in docs/api/client.md and the import path
  (from opendota import OpenDota). Covers the 🤖 AI Summary admonition pattern,
  mkdocs.yml nav, and the mike/CI deploy flow (never deploy by hand).
allowed-tools: Read, Edit, Write, Grep, Bash(uv sync*), Bash(uv run mkdocs*)
---

# Update the mkdocs documentation

Docs are hand-written Markdown in `docs/` (not auto-generated from docstrings even
though `mkdocstrings[python]` is installed). Pages: `docs/index.md`,
`docs/getting-started.md`, `docs/examples.md`, `docs/changelog.md`, and
`docs/api/{client,models,exceptions}.md`. Site config is `mkdocs.yml`.

## Always verify signatures against the code first

The docs have **real drift** — verify every signature against
`src/opendota/client.py` before writing.

Known drift to fix when you touch it: `docs/api/client.md` documents
`get_match(wait_for_replay_url=, reparse_timeout=, reparse_poll_interval=)` and
claims it "raises `ReplayNotAvailableError` by default." The ACTUAL signature is:
```python
def get_match(self, match_id, *, wait_for_replay=False, interval=30.0)
```
It returns a `ParseTask` (awaitable + async-iterable) when `wait_for_replay=True`,
otherwise a coroutine resolving to a `Match`. It does **NOT** raise
`ReplayNotAvailableError`. Correct usage:
```python
match = await client.get_match(8461956309)                       # immediate
match = await client.get_match(8461956309, wait_for_replay=True) # waits for replay
async for status in client.get_match(8461956309, wait_for_replay=True):
    print(f"{status.elapsed:.0f}s, attempt {status.attempts}")
```

`ReplayNotAvailableError` is exported (`from opendota import ...`) and its
docstring still references `wait_for_replay_url`, but **nothing in `client.py`
raises it**. Note this when documenting `docs/api/exceptions.md` — do not claim
`get_match` raises it.

The import path in all examples is `from opendota import OpenDota` (package
`opendota`), never `python_opendota` (that name in `CLAUDE.md`/`RELEASE.md` is
wrong).

## Patterns to preserve

- **AI Summary admonition** — API reference pages open with a collapsible
  `??? info "🤖 AI Summary"` block summarizing the page's methods. Keep this
  pattern and update its contents when you add/change methods. See top of
  `docs/api/client.md`.
- **Material features in use** (from `mkdocs.yml`): red palette, `admonition`,
  `pymdownx.details`/`superfences`/`tabbed`/`highlight`, `tables`, `attr_list`.
  Use fenced ` ```python ` blocks (copy button is enabled).

## Adding a page

New top-level pages must be registered under `nav:` in `mkdocs.yml`. The current
nav: Home, Getting Started, API Reference (Client/Models/Exceptions), Examples,
Changelog.

## Preview locally — never deploy by hand

Install docs deps and serve:
```bash
uv sync --group docs
uv run mkdocs serve
```
Docs deps live in `pyproject.toml [dependency-groups] docs`: `mkdocs-material`,
`mike`, `mkdocstrings[python]`.

**Do NOT run `mike deploy --push` manually.** Deployment is CI-only via
`.github/workflows/docs.yml`, which triggers on pushes to `master` and `v*` tags
that change `docs/**`, `mkdocs.yml`, `src/**`, or the workflow itself:
- push to `master` → `mike deploy --push master`
- release tag `vX` (no `.dev`) → `mike deploy --push --update-aliases X latest`
  then `mike set-default --push latest`
- `.dev` tag → `mike deploy --push X` (version only, no `latest`)

Let the tag/CI handle versioned deploys; a manual `mike deploy` can corrupt the
`gh-pages` version index.
