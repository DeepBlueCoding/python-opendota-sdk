# Changelog

??? info "🤖 AI Summary"

    Version scheme: `{dota_major}.{dota_minor}.{dota_letter}.{sdk_release}` (e.g., 7.40.0 = Dota patch 7.40, initial SDK release). Current version adds: async httpx client, Pydantic models, matches/players/heroes/teams/leagues/pro_players endpoints, error handling, rate limiting, API key support, caching.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [7.40.3] - Unreleased

### Added

- **`ParseTask` class** - Awaitable and async-iterable object for waiting on replay parsing
  - Can be awaited directly: `match = await client.get_match(id, wait_for_replay=True)`
  - Can be iterated for progress: `async for status in client.get_match(id, wait_for_replay=True)`
  - User controls timeout via `break` or `asyncio.timeout()`

- **`ParseStatus` model** - Yielded during `ParseTask` iteration
  - `job_id`: Parse job ID
  - `match_id`: Match being parsed
  - `elapsed`: Seconds since parse request
  - `attempts`: Number of parse attempts

- **`wait_for_replay` parameter in `get_match()`** - Returns `ParseTask` for long-running parses
  - No built-in timeout - user decides when to give up
  - Supports old matches that can take hours to parse
  - `interval` parameter controls polling frequency (default: 30s)

### Changed

- **`get_match()` no longer raises `ReplayNotAvailableError` by default**
  - Returns match data even without `replay_url`
  - Use `wait_for_replay=True` to wait for replay parsing

### Removed

- **`wait_for_replay_url` parameter** - Replaced by `wait_for_replay`
- **`reparse_timeout` parameter** - No built-in timeout, user controls via iteration
- **`reparse_poll_interval` parameter** - Replaced by `interval`
- **`on_progress` callback** - Replaced by async iteration pattern

### Migration

```python
# Old API (7.40.2)
match = await client.get_match(id, wait_for_replay_url=True, reparse_timeout=60)

# New API (7.40.3) - simple await (waits indefinitely)
match = await client.get_match(id, wait_for_replay=True)

# New API (7.40.3) - with user-controlled timeout
async for status in client.get_match(id, wait_for_replay=True):
    if status.elapsed > 60:
        break
```

## [7.40.2] - 2025-12-28

### Added

- **`ReplayNotAvailableError` exception** - Raised when a match's `replay_url` is not available
  - Contains `match_id` attribute for easy identification
  - Provides helpful message suggesting `wait_for_replay_url=True`

- **`request_match(match_id)` method** - Triggers OpenDota to parse/reparse a match
  - Useful when `replay_url` is missing from cached match data
  - Returns job info with `jobId` for tracking

- **`get_parse_job_status(job_id)` method** - Check parse job status
  - Returns `ParseJob` if pending, `None` if completed

## [7.40.1] - 2025-12-16

### Added

#### New Match Fields
- **Team Information**: `radiant_team_id`, `radiant_name`, `radiant_logo`, `radiant_captain`, `dire_team_id`, `dire_name`, `dire_logo`, `dire_captain`, `radiant_team_complete`, `dire_team_complete`
- **Team Objects**: `radiant_team`, `dire_team` (embedded `MatchTeam` models)
- **League Object**: `league` (embedded `MatchLeague` model with `leagueid`, `name`, `tier`, `banner`)
- **Draft Timing**: `draft_timings` (list of `DraftTiming` with pick order, timing, hero selection)
- **Match Analysis**: `comeback`, `stomp`, `pre_game_duration`, `flags`
- **Chat**: `chat` (list of `ChatMessage` with time, type, key, slot)
- **Metadata**: `pauses`, `metadata`, `od_data`, `cosmetics`, `all_word_counts`, `my_word_counts`

#### New Player Fields (within Match)
- **Identity**: `hero_variant`, `personaname`, `name`, `rank_tier`, `is_contributor`, `is_subscriber`
- **Items**: `item_neutral2` (second neutral item slot)
- **Team Context**: `isRadiant`, `radiant_win`, `win`, `lose`, `team_number`, `team_slot`
- **Match Metadata**: `duration`, `game_mode`, `lobby_type`, `cluster`, `patch`, `region`, `start_time`
- **Laning**: `lane`, `lane_role`, `lane_kills`, `lane_efficiency`, `lane_efficiency_pct`, `is_roaming`
- **Party**: `party_id`, `party_size`
- **Combat Stats**: `kda`, `hero_kills`, `tower_kills`, `courier_kills`, `observer_kills`, `sentry_kills`, `roshan_kills`, `ancient_kills`, `neutral_kills`, `necronomicon_kills`
- **Ward Placement**: `obs_placed`, `sen_placed`, `observers_placed`, `observer_uses`, `sentry_uses`
- **Economy**: `total_gold`, `total_xp`, `kills_per_min`, `actions_per_min`
- **Farming**: `camps_stacked`, `creeps_stacked`, `rune_pickups`, `buyback_count`
- **Teamfight**: `teamfight_participation`, `stuns`, `firstblood_claimed`
- **Time Series**: `gold_t`, `xp_t`, `lh_t`, `dn_t`, `times`
- **Detailed Breakdowns**: `benchmarks`, `gold_reasons`, `xp_reasons`, `damage`, `damage_taken`, `damage_inflictor`, `damage_inflictor_received`, `damage_targets`, `hero_hits`, `ability_targets`, `ability_uses`, `ability_upgrades_arr`, `item_uses`, `item_usage`, `item_win`, `purchase`, `purchase_time`, `first_purchase_time`, `actions`, `killed`, `killed_by`, `kill_streaks`, `multi_kills`, `runes`, `healing`, `life_state`, `lane_pos`, `obs`, `sen`, `cosmetics`, `permanent_buffs`, `connection_log`
- **Logs**: `kills_log`, `buyback_log`, `purchase_log`, `runes_log`, `obs_log`, `sen_log`, `obs_left_log`, `sen_left_log`, `neutral_item_history`, `neutral_tokens_log`

#### New Models
- `MatchTeam` - Team data within a match
- `MatchLeague` - League information within a match
- `DraftTiming` - Draft timing data for picks/bans
- `ChatMessage` - Chat message structure

### Changed
- `computed_mmr` type changed from `int` to `float` (API returns decimals)
- `last_login` type changed from `int` to `str` (API returns ISO datetime strings)
- `cosmetics` type changed from `List[int]` to `List[Dict]` (API returns full item details)
- `radiant_logo` and `dire_logo` types changed to `int` (API returns numeric IDs)

### Testing
- Added 29 new tests for new fields (78 total)
- Test coverage for pro matches (TI 2025) and public ranked matches
- Comparison tests between pro and public match data availability

## [7.39.5.2] - 2025-12-15

### Fixed
- Minor bug fixes and stability improvements

## [7.39.5.1.dev2] - 2025-12-03

### Added
- Teams endpoints:
  - `get_teams()` - Get all teams sorted by rating
  - `get_team(team_id)` - Get team details
  - `get_team_players(team_id)` - Get team roster
  - `get_team_matches(team_id)` - Get team match history
- Pro Players endpoints:
  - `get_pro_players()` - Get all professional players
- Leagues endpoints:
  - `get_leagues()` - Get all leagues/tournaments
  - `get_league(league_id)` - Get league details
  - `get_league_matches(league_id)` - Get league matches
  - `get_league_teams(league_id)` - Get teams in a league
- New Pydantic models: `Team`, `TeamPlayer`, `TeamMatch`, `ProPlayer`, `League`
- Comprehensive test suite for new endpoints

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
