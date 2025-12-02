# Client Reference

## OpenDota Class

The main client for interacting with the OpenDota API.

```python
from opendota import OpenDota
```

### Constructor

```python
OpenDota(
    data_dir: Optional[str] = None,
    api_key: Optional[str] = None,
    delay: int = 3,
    fantasy: Optional[Dict[str, float]] = None,
    api_url: Optional[str] = None,
    timeout: float = 30.0,
    format: Literal['pydantic', 'json'] = 'pydantic',
    auth_method: Literal['header', 'query'] = 'header'
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data_dir` | `str` | `~/dota2` | Directory for caching API responses |
| `api_key` | `str` | `None` | OpenDota API key for higher rate limits |
| `delay` | `int` | `3` | Delay between requests (ignored with API key) |
| `timeout` | `float` | `30.0` | Request timeout in seconds |
| `format` | `str` | `'pydantic'` | Response format: `'pydantic'` or `'json'` |
| `auth_method` | `str` | `'header'` | Auth method: `'header'` or `'query'` |

## Match Methods

### get_match

Get detailed match data by match ID.

```python
match = await client.get_match(8461956309)
```

**Parameters:**

- `match_id` (int): The match ID to retrieve

**Returns:** `Match` model or dict

### get_public_matches

Get recent public matches with optional filters.

```python
matches = await client.get_public_matches(
    mmr_ascending=4000,
    less_than_match_id=8461956309
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `mmr_ascending` | `int` | Return matches with avg MMR ascending from this |
| `mmr_descending` | `int` | Return matches with avg MMR descending from this |
| `less_than_match_id` | `int` | Return matches with ID lower than this |

**Returns:** `List[PublicMatch]` or `List[dict]`

### get_pro_matches

Get professional matches.

```python
pro_matches = await client.get_pro_matches()
```

**Parameters:**

- `less_than_match_id` (int, optional): Return matches with ID lower than this

**Returns:** `List[ProMatch]` or `List[dict]`

## Player Methods

### get_player

Get player profile by account ID.

```python
player = await client.get_player(70388657)
```

**Parameters:**

- `account_id` (int): The player's account ID

**Returns:** `PlayerProfile` model or dict

### get_player_matches

Get matches for a player with extensive filtering.

```python
matches = await client.get_player_matches(
    account_id=70388657,
    hero_id=14,  # Pudge
    limit=10,
    win=1  # Only wins
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `account_id` | `int` | Player's account ID (required) |
| `limit` | `int` | Number of matches to return |
| `offset` | `int` | Number of matches to skip |
| `win` | `int` | Filter by wins (0=loss, 1=win) |
| `hero_id` | `int` | Filter by hero ID |
| `game_mode` | `int` | Filter by game mode |
| `lobby_type` | `int` | Filter by lobby type |
| `date` | `int` | Filter by days since epoch |

**Returns:** `List[PlayerMatch]` or `List[dict]`

## Hero Methods

### get_heroes

Get all heroes data.

```python
heroes = await client.get_heroes()
```

**Returns:** `List[Hero]` or `List[dict]`

### get_hero_stats

Get hero statistics including pick/win rates.

```python
hero_stats = await client.get_hero_stats()
```

**Returns:** `List[HeroStats]` or `List[dict]`
