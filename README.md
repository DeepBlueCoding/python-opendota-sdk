# Python OpenDota SDK

[![PyPI version](https://badge.fury.io/py/python-opendota.svg)](https://pypi.org/project/python-opendota/)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://deepbluecoding.github.io/python-opendota-sdk/)
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

## Installation

```bash
pip install python-opendota
```

Or with uv:

```bash
uv add python-opendota
```

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
        print(f"Duration: {match.duration // 60}m {match.duration % 60}s")
        print(f"Winner: {'Radiant' if match.radiant_win else 'Dire'}")

        # Get all heroes
        heroes = await client.get_heroes()
        print(f"Total heroes: {len(heroes)}")

asyncio.run(main())
```

## Authentication

The OpenDota API supports optional API keys for higher rate limits:

```python
# Option 1: Environment variable
export OPENDOTA_API_KEY="your-api-key"

# Option 2: Direct initialization
client = OpenDota(api_key="your-api-key")
```

**Rate Limits:**

- **Free tier**: 2,000 calls/day, 60 calls/minute
- **With API key**: Unlimited calls, higher rate limits

## Output Formats

Choose between structured Pydantic models or raw JSON dictionaries:

```python
# Pydantic models (default) - Full type safety
client = OpenDota(format='pydantic')
matches = await client.get_public_matches()
print(matches[0].match_id)  # Type-safe access

# JSON dictionaries - Direct API response
client = OpenDota(format='json')
matches = await client.get_public_matches()
print(matches[0]['match_id'])  # Dict access
```

## API Reference

### Matches

```python
async with OpenDota() as client:
    # Get detailed match data
    match = await client.get_match(8461956309)

    # Get recent public matches with MMR filter
    high_mmr = await client.get_public_matches(mmr_ascending=4000)

    # Get professional matches
    pro_matches = await client.get_pro_matches()
```

### Players

```python
async with OpenDota() as client:
    # Get player profile
    player = await client.get_player(70388657)
    print(f"Player: {player.profile.personaname}")
    print(f"Rank: {player.rank_tier}")

    # Get player matches with filters
    pudge_matches = await client.get_player_matches(
        account_id=70388657,
        hero_id=14,  # Pudge
        limit=10,
        win=1  # Only wins
    )
```

### Heroes

```python
async with OpenDota() as client:
    # Get all heroes
    heroes = await client.get_heroes()

    # Get hero statistics
    hero_stats = await client.get_hero_stats()
    for hero in hero_stats[:5]:
        if hero.pro_pick:
            winrate = hero.pro_win / hero.pro_pick * 100
            print(f"{hero.localized_name}: {winrate:.1f}% WR")
```

## Available Endpoints

| Category | Method | Description |
|----------|--------|-------------|
| **Matches** | `get_match(match_id)` | Get detailed match data |
| | `get_public_matches(**filters)` | Get public matches |
| | `get_pro_matches(**filters)` | Get professional matches |
| | `get_parsed_matches(**filters)` | Get parsed match data |
| **Players** | `get_player(account_id)` | Get player profile |
| | `get_player_matches(account_id, **filters)` | Get player match history |
| **Heroes** | `get_heroes()` | Get all heroes data |
| | `get_hero_stats()` | Get hero statistics |

## Error Handling

```python
from opendota.exceptions import (
    OpenDotaAPIError,
    OpenDotaNotFoundError,
    OpenDotaRateLimitError
)

try:
    match = await client.get_match(invalid_id)
except OpenDotaNotFoundError:
    print("Match not found")
except OpenDotaRateLimitError:
    print("Rate limit exceeded")
except OpenDotaAPIError as e:
    print(f"API error: {e}")
```

## Development

```bash
# Clone the repository
git clone https://github.com/DeepBlueCoding/python-opendota-sdk.git
cd python-opendota-sdk

# Install with development dependencies
uv sync --group dev

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=opendota

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/ tests/
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Documentation](https://deepbluecoding.github.io/python-opendota-sdk/)
- [PyPI Package](https://pypi.org/project/python-opendota/)
- [GitHub Repository](https://github.com/DeepBlueCoding/python-opendota-sdk)
- [OpenDota API Docs](https://docs.opendota.com/)

## Acknowledgments

- [OpenDota](https://www.opendota.com/) for providing the excellent free API
- [httpx](https://www.python-httpx.org/) for the async HTTP client
- [Pydantic](https://docs.pydantic.dev/) for data validation and parsing
