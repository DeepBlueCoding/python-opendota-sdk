"""Pydantic models for match-related data."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Player(BaseModel):
    """Player data within a match."""
    account_id: Optional[int] = None
    player_slot: int
    hero_id: int
    hero_variant: Optional[int] = None
    item_0: Optional[int] = None
    item_1: Optional[int] = None
    item_2: Optional[int] = None
    item_3: Optional[int] = None
    item_4: Optional[int] = None
    item_5: Optional[int] = None
    backpack_0: Optional[int] = None
    backpack_1: Optional[int] = None
    backpack_2: Optional[int] = None
    item_neutral: Optional[int] = None
    item_neutral2: Optional[int] = None
    kills: int
    deaths: int
    assists: int
    leaver_status: int
    last_hits: int
    denies: int
    gold_per_min: int
    xp_per_min: int
    level: int
    net_worth: Optional[int] = None
    aghanims_scepter: Optional[int] = None
    aghanims_shard: Optional[int] = None
    moonshard: Optional[int] = None
    hero_damage: Optional[int] = None
    tower_damage: Optional[int] = None
    hero_healing: Optional[int] = None
    gold: Optional[int] = None
    gold_spent: Optional[int] = None
    scaled_hero_damage: Optional[int] = None
    scaled_tower_damage: Optional[int] = None
    scaled_hero_healing: Optional[int] = None

    # Player identity
    personaname: Optional[str] = None
    name: Optional[str] = None
    rank_tier: Optional[int] = None
    is_contributor: Optional[bool] = None
    is_subscriber: Optional[bool] = None

    # Team and match context
    isRadiant: Optional[bool] = None
    radiant_win: Optional[bool] = None
    win: Optional[int] = None
    lose: Optional[int] = None
    team_number: Optional[int] = None
    team_slot: Optional[int] = None

    # Match metadata (denormalized)
    duration: Optional[int] = None
    game_mode: Optional[int] = None
    lobby_type: Optional[int] = None
    cluster: Optional[int] = None
    patch: Optional[int] = None
    region: Optional[int] = None
    start_time: Optional[int] = None

    # Laning
    lane: Optional[int] = None
    lane_role: Optional[int] = None
    lane_kills: Optional[int] = None
    lane_efficiency: Optional[float] = None
    lane_efficiency_pct: Optional[int] = None
    is_roaming: Optional[bool] = None

    # Party
    party_id: Optional[int] = None
    party_size: Optional[int] = None

    # Combat stats
    kda: Optional[float] = None
    hero_kills: Optional[int] = None
    tower_kills: Optional[int] = None
    courier_kills: Optional[int] = None
    observer_kills: Optional[int] = None
    sentry_kills: Optional[int] = None
    roshan_kills: Optional[int] = None
    ancient_kills: Optional[int] = None
    neutral_kills: Optional[int] = None
    necronomicon_kills: Optional[int] = None

    # Ward placement
    obs_placed: Optional[int] = None
    sen_placed: Optional[int] = None
    observers_placed: Optional[int] = None
    observer_uses: Optional[int] = None
    sentry_uses: Optional[int] = None

    # Economy
    total_gold: Optional[int] = None
    total_xp: Optional[int] = None
    kills_per_min: Optional[float] = None
    actions_per_min: Optional[int] = None

    # Stacking and farming
    camps_stacked: Optional[int] = None
    creeps_stacked: Optional[int] = None
    rune_pickups: Optional[int] = None

    # Buybacks
    buyback_count: Optional[int] = None

    # Teamfight
    teamfight_participation: Optional[float] = None
    stuns: Optional[float] = None

    # First blood
    firstblood_claimed: Optional[int] = None

    # Misc
    pings: Optional[int] = None
    pred_vict: Optional[bool] = None
    randomed: Optional[bool] = None
    abandons: Optional[int] = None
    last_login: Optional[str] = None
    computed_mmr: Optional[float] = None

    # Time series data
    gold_t: Optional[List[int]] = None
    xp_t: Optional[List[int]] = None
    lh_t: Optional[List[int]] = None
    dn_t: Optional[List[int]] = None
    times: Optional[List[int]] = None

    # Detailed breakdowns (dicts)
    benchmarks: Optional[Dict[str, Any]] = None
    gold_reasons: Optional[Dict[str, int]] = None
    xp_reasons: Optional[Dict[str, int]] = None
    damage: Optional[Dict[str, int]] = None
    damage_taken: Optional[Dict[str, int]] = None
    damage_inflictor: Optional[Dict[str, int]] = None
    damage_inflictor_received: Optional[Dict[str, int]] = None
    damage_targets: Optional[Dict[str, Any]] = None
    hero_hits: Optional[Dict[str, int]] = None
    ability_targets: Optional[Dict[str, Any]] = None
    ability_uses: Optional[Dict[str, int]] = None
    ability_upgrades_arr: Optional[List[int]] = None
    item_uses: Optional[Dict[str, int]] = None
    item_usage: Optional[Dict[str, Any]] = None
    item_win: Optional[Dict[str, int]] = None
    purchase: Optional[Dict[str, int]] = None
    purchase_time: Optional[Dict[str, int]] = None
    first_purchase_time: Optional[Dict[str, int]] = None
    actions: Optional[Dict[str, int]] = None
    killed: Optional[Dict[str, int]] = None
    killed_by: Optional[Dict[str, int]] = None
    kill_streaks: Optional[Dict[str, int]] = None
    multi_kills: Optional[Dict[str, int]] = None
    runes: Optional[Dict[str, int]] = None
    healing: Optional[Dict[str, int]] = None
    life_state: Optional[Dict[str, int]] = None
    life_state_dead: Optional[int] = None
    max_hero_hit: Optional[Dict[str, Any]] = None
    lane_pos: Optional[Dict[str, Any]] = None
    obs: Optional[Dict[str, Any]] = None
    sen: Optional[Dict[str, Any]] = None
    cosmetics: Optional[List[Dict[str, Any]]] = None
    permanent_buffs: Optional[List[Dict[str, Any]]] = None
    connection_log: Optional[List[Dict[str, Any]]] = None

    # Logs
    kills_log: Optional[List[Dict[str, Any]]] = None
    buyback_log: Optional[List[Dict[str, Any]]] = None
    purchase_log: Optional[List[Dict[str, Any]]] = None
    runes_log: Optional[List[Dict[str, Any]]] = None
    obs_log: Optional[List[Dict[str, Any]]] = None
    sen_log: Optional[List[Dict[str, Any]]] = None
    obs_left_log: Optional[List[Dict[str, Any]]] = None
    sen_left_log: Optional[List[Dict[str, Any]]] = None
    neutral_item_history: Optional[List[Dict[str, Any]]] = None
    neutral_tokens_log: Optional[List[Dict[str, Any]]] = None

    # Deprecated/legacy
    purchase_tpscroll: Optional[int] = None
    purchase_ward_sentry: Optional[int] = None
    towers_killed: Optional[int] = None
    roshans_killed: Optional[int] = None


class MatchTeam(BaseModel):
    """Team data within a match."""
    team_id: Optional[int] = None
    name: Optional[str] = None
    tag: Optional[str] = None
    logo_url: Optional[str] = None


class MatchLeague(BaseModel):
    """League information for a match."""
    leagueid: int
    name: Optional[str] = None
    tier: Optional[str] = None
    banner: Optional[str] = None


class PickBan(BaseModel):
    """Pick/ban data for a match."""
    is_pick: bool
    hero_id: int
    team: int
    order: int


class DraftTiming(BaseModel):
    """Draft timing data for a pick/ban."""
    order: int
    pick: bool
    active_team: int
    hero_id: int
    player_slot: Optional[int] = None
    extra_time: Optional[int] = None
    total_time_taken: Optional[int] = None


class ChatMessage(BaseModel):
    """Chat message in a match."""
    time: int
    type: Optional[str] = None
    key: Optional[str] = None
    slot: Optional[int] = None
    player_slot: Optional[int] = None


class Match(BaseModel):
    """Complete match data model."""
    match_id: int
    barracks_status_dire: Optional[int] = None
    barracks_status_radiant: Optional[int] = None
    cluster: Optional[int] = None
    dire_score: int
    duration: int
    engine: Optional[int] = None
    first_blood_time: Optional[int] = None
    game_mode: int
    human_players: Optional[int] = None
    leagueid: Optional[int] = None
    lobby_type: int
    match_seq_num: Optional[int] = None
    negative_votes: Optional[int] = None
    objectives: Optional[List[Dict[str, Any]]] = None
    picks_bans: Optional[List[PickBan]] = None
    positive_votes: Optional[int] = None
    radiant_gold_adv: Optional[List[int]] = None
    radiant_score: int
    radiant_win: bool
    radiant_xp_adv: Optional[List[int]] = None
    start_time: int
    teamfights: Optional[List[Dict[str, Any]]] = None
    tower_status_dire: Optional[int] = None
    tower_status_radiant: Optional[int] = None
    version: Optional[int] = None
    replay_salt: Optional[int] = None
    series_id: Optional[int] = None
    series_type: Optional[int] = None
    players: List[Player]
    patch: Optional[int] = None
    region: Optional[int] = None
    replay_url: Optional[str] = None

    # Team information
    radiant_team_id: Optional[int] = None
    radiant_name: Optional[str] = None
    radiant_logo: Optional[int] = None
    radiant_team: Optional[MatchTeam] = None
    radiant_captain: Optional[int] = None
    radiant_team_complete: Optional[int] = None
    dire_team_id: Optional[int] = None
    dire_name: Optional[str] = None
    dire_logo: Optional[int] = None
    dire_team: Optional[MatchTeam] = None
    dire_captain: Optional[int] = None
    dire_team_complete: Optional[int] = None

    # League information
    league: Optional[MatchLeague] = None

    # Draft timing
    draft_timings: Optional[List[DraftTiming]] = None
    pre_game_duration: Optional[int] = None

    # Match analysis flags
    comeback: Optional[float] = None
    stomp: Optional[float] = None
    flags: Optional[int] = None

    # Chat and cosmetics
    chat: Optional[List[ChatMessage]] = None
    cosmetics: Optional[Dict[str, Any]] = None
    all_word_counts: Optional[Dict[str, int]] = None
    my_word_counts: Optional[Dict[str, int]] = None

    # Pauses and metadata
    pauses: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    od_data: Optional[Dict[str, Any]] = None

    @property
    def start_datetime(self) -> datetime:
        """Convert start_time to datetime object."""
        return datetime.fromtimestamp(self.start_time)


class PublicMatch(BaseModel):
    """Public match data model (simplified)."""
    match_id: int
    match_seq_num: int
    radiant_win: bool
    start_time: int
    duration: int
    avg_mmr: Optional[int] = None
    num_mmr: Optional[int] = None
    lobby_type: int
    game_mode: int
    avg_rank_tier: Optional[float] = None
    num_rank_tier: Optional[int] = None
    cluster: Optional[int] = None

    @property
    def start_datetime(self) -> datetime:
        """Convert start_time to datetime object."""
        return datetime.fromtimestamp(self.start_time)


class ProMatch(BaseModel):
    """Professional match data model."""
    match_id: int
    duration: int
    start_time: int
    radiant_team_id: Optional[int] = None
    radiant_name: Optional[str] = None
    dire_team_id: Optional[int] = None
    dire_name: Optional[str] = None
    leagueid: Optional[int] = None
    league_name: Optional[str] = None
    series_id: Optional[int] = None
    series_type: Optional[int] = None
    radiant_score: int
    dire_score: int
    radiant_win: bool

    @property
    def start_datetime(self) -> datetime:
        """Convert start_time to datetime object."""
        return datetime.fromtimestamp(self.start_time)
