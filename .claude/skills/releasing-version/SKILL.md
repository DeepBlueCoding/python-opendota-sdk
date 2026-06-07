---
name: releasing-version
description: >-
  Cuts a new python-opendota-sdk release: bumps the version in BOTH pyproject.toml
  and src/opendota/__init__.py, updates CHANGELOG.md, and tags so CI publishes to
  PyPI or TestPyPI. Use whenever the user wants to release a new version, bump the
  version, cut a release, publish to PyPI, ship a Dota-patch version (e.g. 7.40.x),
  or make a dev/test release. Encodes the 4-part Dota-patch version scheme from
  VERSIONING.md, the two-places-to-bump rule, and the tag-driven publish logic
  (dash/.dev in tag => TestPyPI, plain tag => PyPI). Ignore the stale RELEASE.md.
disable-model-invocation: true
allowed-tools: Read, Edit, Grep, Bash(git tag*), Bash(git push*), Bash(git status*), Bash(git log*), Bash(uv run python -m build), Bash(uv run twine check*)
---

# Cut a release

Publishing is **tag-driven** via `.github/workflows/publish.yml` (triggers on
tags `v*`). Pushing the right tag is what publishes — bump versions and changelog
first, then tag.

## Ignore RELEASE.md and parts of CLAUDE.md

`RELEASE.md` is stale (cites version `26.0.0` and `src/python_opendota/`). The
authoritative scheme is `VERSIONING.md`; the real version file is
`src/opendota/__init__.py`. Where `CLAUDE.md` says `python_opendota`, it's wrong —
the package is `opendota`, dist name `python-opendota-sdk`.

## Version scheme (VERSIONING.md)

`v{major}.{minor}.{letter}.{sdk_release}` tracking the Dota 2 patch.
`letter`: 0=none, 1=a, 2=b, 3=c, ... — e.g. `7.39.5.1` = patch 7.39e, first SDK
release; `7.39.5.2` = bugfix, still 7.39e; `7.40.0.1` = patch 7.40, first release.
- **New Dota patch** → bump `major.minor.letter`, reset `sdk_release` to 1.
- **SDK-only fix or feature** → increment `sdk_release`.

Note a real discrepancy: the current shipped version is `7.40.3` (three parts in
both `pyproject.toml` and `src/opendota/__init__.py`), which does not match the
4-part scheme. Confirm the intended next version with the user if it's ambiguous,
and keep the two files identical to whatever you pick.

## Workflow

1. Pick the version per VERSIONING.md.
2. Bump it in **two places, identically**:
   - `pyproject.toml` → `[project] version = "X.Y.Z..."`
   - `src/opendota/__init__.py` → `__version__ = "X.Y.Z..."`
3. Update `CHANGELOG.md`.
4. Commit and get it onto `master` (branch + PR if not already there — only
   commit/push when the user asks).
5. Tag and push to trigger publish:
   ```bash
   git tag vX.Y.Z          # NO dash  -> PyPI (publish-pypi job)
   git push origin vX.Y.Z
   ```
   For a test release:
   ```bash
   git tag vX.Y.Z-dev1     # has '-' (or '.dev') -> TestPyPI (publish-test-pypi)
   git push origin vX.Y.Z-dev1
   ```

## Tag → destination logic (publish.yml)

- Tag **without** `-` and **without** `.dev` → **PyPI**.
- Tag **with** `-` or `.dev` → **TestPyPI**.

So `vX.Y.Z.W` → PyPI; `vX.Y.Z.W-dev1` → TestPyPI.

## CI gates before publish

The `test` job runs `uv run pytest tests/ -v` on Python 3.9–3.12, then `build`
runs `uv run python -m build` and `uv run twine check dist/*`. **CI tests hit the
LIVE OpenDota API**, so a transient API change can fail a release build even with
no code bug — re-run the job or fix the affected golden value if the API genuinely
changed.

Publishing uses **PyPI trusted publishing** (`permissions: id-token: write`,
`pypa/gh-action-pypi-publish`) — no upload secrets in CI. Manual `twine upload` is
only a fallback.

## Local pre-flight (optional, safe to run)

```bash
uv run python -m build
uv run twine check dist/*
```
Build backend is `hatchling`; the wheel packages `["src/opendota"]`
(`pyproject.toml [tool.hatch.build.targets.wheel]`). Always use `uv` per
`CLAUDE.md` — never `pip`/`python` directly.

## Checklist

- [ ] Version chosen per VERSIONING.md
- [ ] `pyproject.toml` version bumped
- [ ] `src/opendota/__init__.py` `__version__` bumped to the SAME string
- [ ] `CHANGELOG.md` updated
- [ ] Committed to master
- [ ] Tag pushed (`-`/`.dev` for TestPyPI, plain for PyPI)
