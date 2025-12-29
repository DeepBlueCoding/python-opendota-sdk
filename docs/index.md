# Python OpenDota SDK

??? info "🤖 AI Summary"

    Async Python SDK for OpenDota API. Use `OpenDota()` as async context manager. Key methods: `get_match(id)`, `get_player(id)`, `get_public_matches()`, `get_heroes()`. Returns Pydantic models by default (type-safe), or dicts with `format='json'`. Free tier: 2000 calls/day. Install: `pip install python-opendota-sdk`.

> Modern async Python wrapper for the OpenDota API

[![PyPI version](https://badge.fury.io/py/python-opendota-sdk.svg)](https://pypi.org/project/python-opendota-sdk/)
[![Build Status](https://github.com/DeepBlueCoding/python-opendota-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/DeepBlueCoding/python-opendota-sdk/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A modern, async Python wrapper for the [OpenDota API](https://docs.opendota.com/) with full type safety and comprehensive coverage.

## Features

- **Async/await support** - Built with `httpx` for modern async Python applications
- **Type safety** - Full type hints and Pydantic models for all API responses
- **Comprehensive coverage** - Support for matches, players, heroes, and more endpoints
- **Rate limiting aware** - Handles API rate limits gracefully with proper error handling
- **Simple API** - Clean, intuitive interface following Python best practices
- **Well tested** - Comprehensive test suite with real API integration tests
- **Python 3.9+** - Compatible with modern Python versions

## Quick Start

```python
import asyncio
from opendota import OpenDota

async def main():
    async with OpenDota() as client:
        # Get recent public matches
        matches = await client.get_public_matches()
        print(f"Found {len(matches)} recent matches")

        # Get detailed match data
        match = await client.get_match(matches[0].match_id)
        print(f"Match duration: {match.duration // 60}m")

        # Get all heroes
        heroes = await client.get_heroes()
        print(f"Total heroes: {len(heroes)}")

asyncio.run(main())
```

### Fetching Match Replays

Replay URLs are not immediately available for all matches. OpenDota must first download and parse the replay from Valve's servers, which can take time. By default, `get_match()` raises a `ReplayNotAvailableError` if the replay URL is missing.

Use `wait_for_replay_url=True` to automatically request a parse and poll until the replay URL becomes available:

```python
from opendota import OpenDota
from opendota.exceptions import ReplayNotAvailableError

async with OpenDota() as client:
    try:
        # Wait for replay to be parsed (up to 60 seconds)
        match = await client.get_match(
            match_id=7891234567,
            wait_for_replay_url=True,
            reparse_timeout=60.0,
        )
        print(f"Replay URL: {match.replay_url}")
    except ReplayNotAvailableError:
        print("Replay not available after timeout")
```

## Installation

```bash
pip install python-opendota-sdk
```

Or with uv:

```bash
uv add python-opendota-sdk
```

## Links

- [GitHub Repository](https://github.com/DeepBlueCoding/python-opendota-sdk)
- [PyPI Package](https://pypi.org/project/python-opendota-sdk/)
- [OpenDota API Docs](https://docs.opendota.com/)
