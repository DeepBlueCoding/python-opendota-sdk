# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [7.39.5.1] - 2025-12-02

Version scheme: `{dota_major}.{dota_minor}.{dota_letter}.{sdk_release}`
- `7.39.5` = Dota 2 patch 7.39e (a=1, b=2, c=3, d=4, e=5)
- `.1` = First SDK release for this patch

### Added
- Full async/await support with httpx
- Complete type safety with Pydantic models
- Matches endpoints:
  - `get_match()` - Get detailed match data
  - `get_public_matches()` - Get public matches with filters
  - `get_pro_matches()` - Get professional matches
  - `get_parsed_matches()` - Get parsed match data
- Players endpoints:
  - `get_player()` - Get player profile
  - `get_player_matches()` - Get player match history with extensive filtering
- Heroes endpoints:
  - `get_heroes()` - Get all heroes data
  - `get_hero_stats()` - Get hero statistics
- Comprehensive error handling with custom exceptions
- Rate limiting awareness and proper HTTP status handling
- Optional API key support for higher rate limits
- Context manager support for automatic cleanup
- Built-in response caching
- Extensive test suite with real API integration tests
- Full documentation with MkDocs Material theme

### Technical Details
- Python 3.9+ support
- Built with httpx for modern async HTTP
- Pydantic v2 for data validation and parsing
- Comprehensive type hints throughout
- CI/CD with GitHub Actions
- TestPyPI and PyPI publishing support
