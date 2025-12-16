# Data Models

??? info "🤖 AI Summary"

    Pydantic models for API responses. **Match models**: `Match` (full data with players, teams, league, draft), `PublicMatch` (summary with avg_mmr), `ProMatch` (with team/league names). **Player models**: `PlayerProfile` (profile + rank_tier), `PlayerMatch` (hero_id, KDA, player_slot), `Player` (detailed match player with laning, combat, economy data). **Hero models**: `Hero` (name, roles, primary_attr), `HeroStats` (pro_pick/win/ban, rank-specific picks). **New in 7.40**: Team objects, league objects, draft timings, chat messages, detailed player analytics.

All API responses are parsed into Pydantic models with full type safety.

## Match Models

### Match

Detailed match data returned by `get_match()`.

```python
class Match(BaseModel):
    match_id: int
    duration: int
    radiant_win: bool
    radiant_score: int
    dire_score: int
    players: List[Player]

    # Team information (pro matches)
    radiant_team_id: Optional[int]
    radiant_name: Optional[str]
    dire_team_id: Optional[int]
    dire_name: Optional[str]
    radiant_team: Optional[MatchTeam]
    dire_team: Optional[MatchTeam]

    # League information
    league: Optional[MatchLeague]

    # Draft (Captains Mode)
    draft_timings: Optional[List[DraftTiming]]

    # Analysis
    comeback: Optional[float]
    stomp: Optional[float]

    # Chat
    chat: Optional[List[ChatMessage]]
```

**Core Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `match_id` | `int` | Unique match identifier |
| `duration` | `int` | Match duration in seconds |
| `radiant_win` | `bool` | Whether Radiant won |
| `radiant_score` | `int` | Radiant kill score |
| `dire_score` | `int` | Dire kill score |
| `players` | `List[Player]` | List of player data |
| `game_mode` | `int` | Game mode ID |
| `lobby_type` | `int` | Lobby type ID |

**Team Fields (Pro Matches):**

| Field | Type | Description |
|-------|------|-------------|
| `radiant_team_id` | `Optional[int]` | Radiant team ID |
| `radiant_name` | `Optional[str]` | Radiant team name |
| `radiant_logo` | `Optional[int]` | Radiant team logo ID |
| `radiant_captain` | `Optional[int]` | Radiant captain account ID |
| `dire_team_id` | `Optional[int]` | Dire team ID |
| `dire_name` | `Optional[str]` | Dire team name |
| `dire_logo` | `Optional[int]` | Dire team logo ID |
| `dire_captain` | `Optional[int]` | Dire captain account ID |

**Match Analysis Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `comeback` | `Optional[float]` | Comeback indicator score |
| `stomp` | `Optional[float]` | Stomp indicator score |
| `pre_game_duration` | `Optional[int]` | Pre-game phase duration |
| `flags` | `Optional[int]` | Match flags |

### MatchTeam

Team data embedded within a match.

```python
class MatchTeam(BaseModel):
    team_id: Optional[int]
    name: Optional[str]
    tag: Optional[str]
    logo_url: Optional[str]
```

### MatchLeague

League information embedded within a match.

```python
class MatchLeague(BaseModel):
    leagueid: int
    name: Optional[str]
    tier: Optional[str]  # "premium", "professional", "amateur"
    banner: Optional[str]
```

### DraftTiming

Draft timing data for each pick/ban in Captains Mode.

```python
class DraftTiming(BaseModel):
    order: int              # Draft order (0-23)
    pick: bool              # True if pick, False if ban
    active_team: int        # Team making the selection
    hero_id: int            # Hero selected
    player_slot: Optional[int]
    extra_time: Optional[int]
    total_time_taken: Optional[int]
```

### ChatMessage

Chat message in a match.

```python
class ChatMessage(BaseModel):
    time: int               # Game time in seconds
    type: Optional[str]     # Message type
    key: Optional[str]      # Chat wheel key or message
    slot: Optional[int]     # Player slot
    player_slot: Optional[int]
```

### Player (Match Player)

Detailed player data within a match. Contains extensive analytics for parsed matches.

```python
class Player(BaseModel):
    # Core stats
    account_id: Optional[int]
    player_slot: int
    hero_id: int
    kills: int
    deaths: int
    assists: int

    # New identity fields
    hero_variant: Optional[int]     # Hero persona/arcana variant
    personaname: Optional[str]      # Display name
    isRadiant: Optional[bool]       # Team indicator

    # Items
    item_0: Optional[int]
    item_1: Optional[int]
    # ... item_2 through item_5
    item_neutral: Optional[int]     # First neutral item
    item_neutral2: Optional[int]    # Second neutral item (new)

    # Laning
    lane: Optional[int]             # 1=safe, 2=mid, 3=off
    lane_role: Optional[int]        # Lane role
    lane_efficiency: Optional[float]
    is_roaming: Optional[bool]

    # Combat
    kda: Optional[float]            # Calculated KDA ratio
    tower_kills: Optional[int]
    teamfight_participation: Optional[float]
    stuns: Optional[float]

    # Support stats
    obs_placed: Optional[int]       # Observer wards placed
    sen_placed: Optional[int]       # Sentry wards placed
    camps_stacked: Optional[int]

    # Time series (parsed matches)
    gold_t: Optional[List[int]]     # Gold per minute
    xp_t: Optional[List[int]]       # XP per minute
    lh_t: Optional[List[int]]       # Last hits per minute

    # Detailed breakdowns
    benchmarks: Optional[Dict]      # Performance benchmarks
    ability_uses: Optional[Dict]    # Ability usage counts
    damage: Optional[Dict]          # Damage dealt breakdown
```

**Identity Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `hero_variant` | `Optional[int]` | Hero persona/arcana variant |
| `personaname` | `Optional[str]` | Player display name |
| `name` | `Optional[str]` | Pro player name |
| `isRadiant` | `Optional[bool]` | True if on Radiant team |
| `rank_tier` | `Optional[int]` | Player rank tier |

**Laning Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `lane` | `Optional[int]` | Lane (1=safe, 2=mid, 3=off) |
| `lane_role` | `Optional[int]` | Role in lane |
| `lane_efficiency` | `Optional[float]` | Laning efficiency (0-1) |
| `lane_kills` | `Optional[int]` | Kills during laning |
| `is_roaming` | `Optional[bool]` | Roaming indicator |

**Combat Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `kda` | `Optional[float]` | KDA ratio |
| `hero_kills` | `Optional[int]` | Hero kills |
| `tower_kills` | `Optional[int]` | Tower kills |
| `roshan_kills` | `Optional[int]` | Roshan kills |
| `teamfight_participation` | `Optional[float]` | Teamfight participation (0-1) |
| `stuns` | `Optional[float]` | Stun duration dealt |

**Support Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `obs_placed` | `Optional[int]` | Observer wards placed |
| `sen_placed` | `Optional[int]` | Sentry wards placed |
| `camps_stacked` | `Optional[int]` | Camps stacked |
| `rune_pickups` | `Optional[int]` | Runes picked up |

### PublicMatch

Summary data for public matches.

```python
class PublicMatch(BaseModel):
    match_id: int
    duration: int
    radiant_win: bool
    avg_mmr: Optional[int]
    avg_rank_tier: Optional[float]
    game_mode: int
    lobby_type: int
```

### ProMatch

Professional match data.

```python
class ProMatch(BaseModel):
    match_id: int
    duration: int
    radiant_win: bool
    radiant_name: Optional[str]
    dire_name: Optional[str]
    radiant_team_id: Optional[int]
    dire_team_id: Optional[int]
    league_name: Optional[str]
    leagueid: Optional[int]
```

## Player Models

### PlayerProfile

Player profile and ranking data.

```python
class PlayerProfile(BaseModel):
    profile: Profile
    rank_tier: Optional[int]
    leaderboard_rank: Optional[int]
```

**Profile Sub-model:**

```python
class Profile(BaseModel):
    account_id: int
    personaname: Optional[str]
    name: Optional[str]
    steamid: Optional[str]
    avatar: Optional[str]
    loccountrycode: Optional[str]
    plus: Optional[bool]           # Dota Plus subscriber
    is_contributor: Optional[bool]
    is_subscriber: Optional[bool]
```

### PlayerMatch

Match data from player's perspective (player match history).

```python
class PlayerMatch(BaseModel):
    match_id: int
    hero_id: int
    kills: int
    deaths: int
    assists: int
    player_slot: int
    radiant_win: bool
    duration: int
    game_mode: int
    hero_variant: Optional[int]    # New in 7.40
```

## Hero Models

### Hero

Basic hero information.

```python
class Hero(BaseModel):
    id: int
    name: str                      # Internal name (e.g., "npc_dota_hero_antimage")
    localized_name: str            # Display name (e.g., "Anti-Mage")
    primary_attr: str              # "agi", "str", "int", "all"
    attack_type: str               # "Melee" or "Ranged"
    roles: List[str]               # ["Carry", "Escape", "Nuker"]
```

### HeroStats

Hero statistics with pick/win rates across skill brackets.

```python
class HeroStats(BaseModel):
    id: int
    localized_name: str
    pro_pick: Optional[int]
    pro_win: Optional[int]
    pro_ban: Optional[int]
    pub_pick: Optional[int]
    pub_win: Optional[int]
    # Per-rank stats (1-8)
    field_1_pick: Optional[int]    # Herald picks
    field_1_win: Optional[int]     # Herald wins
    # ... through field_8_pick/win (Immortal)
    pub_pick_trend: Optional[List[int]]
    pub_win_trend: Optional[List[int]]
```

## Usage Examples

### Basic Match Analysis

```python
from opendota import OpenDota

async with OpenDota() as client:
    match = await client.get_match(8461956309)

    # Access basic properties
    print(f"Duration: {match.duration}s")
    print(f"Winner: {'Radiant' if match.radiant_win else 'Dire'}")

    # Access team info (pro matches)
    if match.radiant_name:
        print(f"Teams: {match.radiant_name} vs {match.dire_name}")

    # Access league info
    if match.league:
        print(f"Tournament: {match.league.name} ({match.league.tier})")
```

### Detailed Player Analysis

```python
async with OpenDota() as client:
    match = await client.get_match(8461956309)

    for player in match.players:
        team = "Radiant" if player.isRadiant else "Dire"
        print(f"[{team}] {player.personaname}")
        print(f"  Hero variant: {player.hero_variant}")
        print(f"  KDA: {player.kda:.2f}")
        print(f"  Lane: {player.lane}, Efficiency: {player.lane_efficiency:.1%}")

        if player.obs_placed:
            print(f"  Wards: {player.obs_placed} obs, {player.sen_placed} sen")

        if player.gold_t:
            print(f"  Final gold: {player.gold_t[-1]}")
```

### Draft Analysis

```python
async with OpenDota() as client:
    match = await client.get_match(8461956309)

    if match.draft_timings:
        print("Draft order:")
        for draft in match.draft_timings:
            action = "PICK" if draft.pick else "BAN"
            team = "Radiant" if draft.active_team == 0 else "Dire"
            print(f"  {draft.order}: [{team}] {action} hero {draft.hero_id}")
```

### Pro vs Public Match Data

```python
async with OpenDota() as client:
    # Pro match - has team/league/draft data
    pro = await client.get_match(8461956309)
    print(f"Pro match: {pro.radiant_name} vs {pro.dire_name}")
    print(f"League: {pro.league.name}")
    print(f"Draft entries: {len(pro.draft_timings)}")

    # Public match - limited metadata
    pub = await client.get_match(8607246638)
    print(f"Public match: Team info = {pub.radiant_name}")  # None
    print(f"League: {pub.league}")  # None
    print(f"Draft: {pub.draft_timings}")  # None or empty
```
