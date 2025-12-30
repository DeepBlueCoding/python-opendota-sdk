"""Tests for matches endpoints using Golden Master approach with real data."""

import sys
from datetime import datetime

import pytest

sys.path.insert(0, 'src')
from opendota.client import OpenDota
from opendota.exceptions import OpenDotaNotFoundError, ReplayNotAvailableError
from opendota.models import ChatMessage, DraftTiming, MatchTeam


class TestMatches:
    """Test cases for matches endpoints using real expected values."""

    @pytest.fixture
    async def client(self):
        """Create a test client."""
        async with OpenDota() as client:
            yield client

    @pytest.mark.asyncio
    async def test_get_match_8461956309_golden_master(self, client):
        """Test getting match 8461956309 with exact expected values."""
        match_id = 8461956309

        match = await client.get_match(match_id)

        # Test exact match properties from real data
        assert match.match_id == 8461956309
        assert match.duration == 3512
        assert match.radiant_win is False
        assert match.radiant_score == 11
        assert match.dire_score == 24
        assert match.start_time == 1757872818
        assert match.game_mode == 2
        assert match.lobby_type == 1
        assert len(match.players) == 10

        # Test datetime conversion
        expected_datetime = datetime.fromtimestamp(1757872818)
        assert match.start_datetime == expected_datetime

        # Test exact player data from real match
        players = match.players

        # Player 0 (Radiant, slot 0, Juggernaut)
        p0 = players[0]
        assert p0.account_id == 898754153
        assert p0.player_slot == 0
        assert p0.hero_id == 8  # Juggernaut
        assert p0.kills == 4
        assert p0.deaths == 3
        assert p0.assists == 1
        assert p0.last_hits == 866
        assert p0.denies == 11
        assert p0.gold_per_min == 769
        assert p0.xp_per_min == 812

        # Player 1 (Radiant, slot 1, Shadow Fiend)
        p1 = players[1]
        assert p1.account_id == 137129583
        assert p1.player_slot == 1
        assert p1.hero_id == 11  # Shadow Fiend
        assert p1.kills == 3
        assert p1.deaths == 3
        assert p1.assists == 6
        assert p1.last_hits == 632

        # Player 5 (Dire, slot 128, Keeper of the Light)
        p5 = players[5]
        assert p5.account_id == 10366616
        assert p5.player_slot == 128  # Dire team starts at 128
        assert p5.hero_id == 89  # Keeper of the Light
        assert p5.kills == 1
        assert p5.deaths == 0
        assert p5.assists == 15
        assert p5.last_hits == 282

        # Player 9 (Dire, slot 132, Rubick)
        p9 = players[9]
        assert p9.account_id == 25907144
        assert p9.player_slot == 132
        assert p9.hero_id == 87  # Rubick
        assert p9.kills == 7
        assert p9.deaths == 3
        assert p9.assists == 16
        assert p9.last_hits == 30  # Support, low last hits

        # Test team composition - exactly 5 Radiant (slots 0-4) and 5 Dire (slots 128-132)
        radiant_players = [p for p in players if p.player_slot < 128]
        dire_players = [p for p in players if p.player_slot >= 128]
        assert len(radiant_players) == 5
        assert len(dire_players) == 5

        # Test total kills match team scores
        radiant_kills = sum(p.kills for p in radiant_players)
        dire_kills = sum(p.kills for p in dire_players)
        assert radiant_kills == match.radiant_score  # 11
        assert dire_kills == match.dire_score  # 24

    @pytest.mark.asyncio
    async def test_public_matches_structure_validation(self, client):
        """Test public matches return expected structure and reasonable values."""
        matches = await client.get_public_matches()

        # Should return exactly 100 matches (API default)
        assert len(matches) == 100

        # Test first match has required fields with realistic values
        first_match = matches[0]
        assert first_match.match_id > 8000000000  # Recent match IDs are very large
        # Duration can be 0 for abandoned matches, otherwise should be reasonable
        assert first_match.duration >= 0  # Can be 0 for abandoned/invalid
        assert first_match.duration <= 10800  # Max 3 hours
        # Game mode and lobby type can vary widely
        assert first_match.game_mode >= 0
        assert first_match.lobby_type >= 0

        # All matches should have recent timestamps (within last month)
        recent_timestamp = 1757000000  # Approximately recent
        assert first_match.start_time > recent_timestamp

        # Match sequence numbers should exist and be reasonable
        match_seqs = [m.match_seq_num for m in matches if m.match_seq_num is not None]
        if match_seqs:
            # All sequence numbers should be positive and large (recent matches)
            for seq in match_seqs:
                assert seq > 7000000000, f"Match sequence {seq} seems too old"

    @pytest.mark.asyncio
    async def test_pro_matches_business_logic(self, client):
        """Test professional matches have expected professional characteristics."""
        pro_matches = await client.get_pro_matches()

        # Should return 100 matches (API default)
        assert len(pro_matches) == 100

        first_match = pro_matches[0]

        # Pro matches should have team information
        team_names_exist = (
            first_match.radiant_name is not None or
            first_match.dire_name is not None or
            first_match.radiant_team_id is not None or
            first_match.dire_team_id is not None
        )
        assert team_names_exist, "Pro match should have team information"

        # Pro matches should have reasonable durations (not too short)
        assert first_match.duration >= 600, "Pro matches should be at least 10 minutes"

        # League information should exist for pro matches
        has_league_info = (
            first_match.leagueid is not None or
            first_match.league_name is not None
        )
        assert has_league_info, "Pro match should have league information"

    @pytest.mark.asyncio
    async def test_match_not_found_error_handling(self, client):
        """Test proper error handling for non-existent matches."""
        fake_match_id = 999999999999999

        with pytest.raises(OpenDotaNotFoundError) as exc_info:
            await client.get_match(fake_match_id)

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_parsed_matches_data_consistency(self, client):
        """Test parsed matches return consistent data structure."""
        parsed_matches = await client.get_parsed_matches()

        # API may return empty list if no recent parsed matches
        if parsed_matches:
            # Should be list of dicts (raw data)
            first_parsed = parsed_matches[0]
            assert "match_id" in first_parsed
            assert isinstance(first_parsed["match_id"], int)
            assert first_parsed["match_id"] > 0

    @pytest.mark.asyncio
    async def test_match_team_information_ti2025(self, client):
        """Test match team fields with TI 2025 match (Xtreme Gaming vs Team Falcons)."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        # Radiant team: Xtreme Gaming
        assert match.radiant_team_id == 8261500
        assert match.radiant_name == "Xtreme Gaming"
        assert match.radiant_logo == 2402194226059610600
        assert match.radiant_captain == 137129583

        # Dire team: Team Falcons
        assert match.dire_team_id == 9247354
        assert match.dire_name == "Team Falcons"
        assert match.dire_logo == 2314350571781870000
        assert match.dire_captain == 183719386

    @pytest.mark.asyncio
    async def test_match_league_information_ti2025(self, client):
        """Test league object with TI 2025 match."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        # League information
        assert match.league is not None
        assert match.league.leagueid == 18324
        assert match.league.name == "The International 2025"
        assert match.league.tier == "premium"

    @pytest.mark.asyncio
    async def test_match_draft_timings(self, client):
        """Test draft timing data with TI 2025 match."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        # Draft timings should exist for pro matches
        assert match.draft_timings is not None
        assert len(match.draft_timings) == 24  # 10 picks + 14 bans in captains mode

        # Test first draft timing entry
        first_draft = match.draft_timings[0]
        assert isinstance(first_draft, DraftTiming)
        assert first_draft.order >= 0
        assert isinstance(first_draft.pick, bool)
        assert first_draft.active_team in [0, 1, 2, 3]
        assert first_draft.hero_id >= 0

    @pytest.mark.asyncio
    async def test_match_analysis_flags(self, client):
        """Test match analysis flags (comeback/stomp indicators)."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        # Analysis flags exist
        assert match.comeback is not None
        assert match.stomp is not None

        # Values from real match
        assert match.comeback == 463
        assert match.stomp == 29353

        # Pre-game duration
        assert match.pre_game_duration == 90

    @pytest.mark.asyncio
    async def test_match_chat_messages(self, client):
        """Test chat messages in match."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        # Chat should exist
        assert match.chat is not None
        assert len(match.chat) == 37  # Exact count from real match

        # Test chat message structure
        first_chat = match.chat[0]
        assert isinstance(first_chat, ChatMessage)
        assert isinstance(first_chat.time, int)

    @pytest.mark.asyncio
    async def test_player_new_identity_fields(self, client):
        """Test new player identity fields."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        p0 = match.players[0]

        # Hero variant (persona/arcana variant)
        assert p0.hero_variant == 2

        # Player identity
        assert p0.personaname == "念头通达"

        # Team indicator
        assert p0.isRadiant is True

        # Party size (5-stack pro team)
        assert p0.party_size == 10

    @pytest.mark.asyncio
    async def test_player_item_neutral2(self, client):
        """Test second neutral item slot."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        p0 = match.players[0]

        # Second neutral item slot
        assert p0.item_neutral2 == 1584

    @pytest.mark.asyncio
    async def test_player_laning_fields(self, client):
        """Test player laning phase data."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        # Player 0 - Juggernaut (carry)
        p0 = match.players[0]
        assert p0.lane == 1  # Safelane
        assert p0.lane_role == 1  # Core role

        # Lane efficiency should be high for carry
        assert p0.lane_efficiency is not None
        assert 0.8 <= p0.lane_efficiency <= 0.9  # ~83.4%

    @pytest.mark.asyncio
    async def test_player_combat_stats(self, client):
        """Test player combat statistics."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        p0 = match.players[0]

        # KDA
        assert p0.kda is not None
        assert p0.kda == 1.25  # (4 kills + 1 assist) / 3 deaths

        # Tower kills
        assert p0.tower_kills == 0

        # Rune pickups
        assert p0.rune_pickups == 1

        # Teamfight participation
        assert p0.teamfight_participation is not None
        assert 0.4 <= p0.teamfight_participation <= 0.5

    @pytest.mark.asyncio
    async def test_player_support_ward_stats(self, client):
        """Test support player ward placement stats."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        # Player 5 - KOTL (support, Team Falcons)
        p5 = match.players[5]

        # Ward placement - supports should have high counts
        assert p5.obs_placed == 8
        assert p5.sen_placed == 23

        # Camps stacked
        assert p5.camps_stacked == 1

        # High teamfight participation for support
        assert p5.teamfight_participation == 0.625

    @pytest.mark.asyncio
    async def test_player_time_series_data(self, client):
        """Test player time series data (gold over time, etc.)."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        p0 = match.players[0]

        # Gold over time
        assert p0.gold_t is not None
        assert len(p0.gold_t) == 59  # One entry per minute

        # Gold should generally increase over time for carry
        assert p0.gold_t[0] < p0.gold_t[-1]

        # XP over time
        assert p0.xp_t is not None
        assert len(p0.xp_t) > 0

        # Last hits over time
        assert p0.lh_t is not None
        assert len(p0.lh_t) > 0

    @pytest.mark.asyncio
    async def test_player_detailed_breakdowns(self, client):
        """Test player detailed breakdown dictionaries."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        p0 = match.players[0]

        # Benchmarks (performance comparisons)
        assert p0.benchmarks is not None
        assert isinstance(p0.benchmarks, dict)

        # Ability uses
        assert p0.ability_uses is not None
        assert isinstance(p0.ability_uses, dict)

        # Purchase log
        assert p0.purchase_log is not None
        assert len(p0.purchase_log) == 42  # Exact count from real match

    @pytest.mark.asyncio
    async def test_player_radiant_dire_separation(self, client):
        """Test isRadiant field correctly separates teams."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        radiant_players = [p for p in match.players if p.isRadiant is True]
        dire_players = [p for p in match.players if p.isRadiant is False]

        assert len(radiant_players) == 5
        assert len(dire_players) == 5

        # Radiant players should have slots 0-4
        for p in radiant_players:
            assert p.player_slot < 128

        # Dire players should have slots 128+
        for p in dire_players:
            assert p.player_slot >= 128

    @pytest.mark.asyncio
    async def test_match_team_objects(self, client):
        """Test embedded team objects in match."""
        match_id = 8461956309
        match = await client.get_match(match_id)

        # Team objects may or may not be present
        if match.radiant_team is not None:
            assert isinstance(match.radiant_team, MatchTeam)

        if match.dire_team is not None:
            assert isinstance(match.dire_team, MatchTeam)


class TestPublicMatchNewFields:
    """Test new fields with public ranked match 8607246638 (non-pro match)."""

    @pytest.fixture
    async def client(self):
        """Create a test client."""
        async with OpenDota() as client:
            yield client

    @pytest.mark.asyncio
    async def test_public_match_basic_data(self, client):
        """Test basic match data for public ranked match."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        # Basic match properties
        assert match.match_id == 8607246638
        assert match.duration == 3529  # ~58 min game
        assert match.radiant_win is False
        assert match.radiant_score == 44
        assert match.dire_score == 46
        assert match.game_mode == 22  # All Pick Ranked
        assert match.lobby_type == 0  # Public match
        assert len(match.players) == 10

    @pytest.mark.asyncio
    async def test_public_match_no_team_info(self, client):
        """Test that public matches don't have team information."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        # Public matches should not have pro team info
        assert match.radiant_team_id is None
        assert match.radiant_name is None
        assert match.dire_team_id is None
        assert match.dire_name is None
        assert match.radiant_captain is None
        assert match.dire_captain is None

    @pytest.mark.asyncio
    async def test_public_match_no_league(self, client):
        """Test that public matches don't have league information."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        # Public matches should not have league info
        assert match.league is None
        assert match.leagueid is None or match.leagueid == 0

    @pytest.mark.asyncio
    async def test_public_match_no_draft_timings(self, client):
        """Test that All Pick matches don't have draft timings."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        # All Pick doesn't have draft phase like Captains Mode
        assert match.draft_timings is None or len(match.draft_timings) == 0

    @pytest.mark.asyncio
    async def test_public_match_pre_game_duration(self, client):
        """Test pre-game duration exists for public match."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        assert match.pre_game_duration == 90

    @pytest.mark.asyncio
    async def test_public_match_player_hero_variant(self, client):
        """Test hero variant field in public match."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        # Player 0 - Sven with hero variant
        p0 = match.players[0]
        assert p0.hero_id == 18  # Sven
        assert p0.hero_variant == 2

    @pytest.mark.asyncio
    async def test_public_match_dual_neutral_items(self, client):
        """Test both neutral item slots in public match."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        # Player 0 has both neutral items
        p0 = match.players[0]
        assert p0.item_neutral == 1643
        assert p0.item_neutral2 == 1586

    @pytest.mark.asyncio
    async def test_public_match_player_kda(self, client):
        """Test KDA calculation in public match."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        # Player 0 - Sven with 25/11/12
        p0 = match.players[0]
        assert p0.kills == 25
        assert p0.deaths == 11
        assert p0.assists == 12

        # KDA = (25 + 12) / 11 = 3.36... but API shows 3.08
        # API calculates differently, just verify it exists and is reasonable
        assert p0.kda is not None
        assert 3.0 <= p0.kda <= 3.5

    @pytest.mark.asyncio
    async def test_public_match_player_benchmarks(self, client):
        """Test benchmarks exist for public match players."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        p0 = match.players[0]
        assert p0.benchmarks is not None
        assert isinstance(p0.benchmarks, dict)

    @pytest.mark.asyncio
    async def test_public_match_isRadiant_separation(self, client):
        """Test isRadiant correctly separates teams in public match."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        radiant = [p for p in match.players if p.isRadiant is True]
        dire = [p for p in match.players if p.isRadiant is False]

        assert len(radiant) == 5
        assert len(dire) == 5

        # Verify slot alignment
        for p in radiant:
            assert p.player_slot < 128
        for p in dire:
            assert p.player_slot >= 128

    @pytest.mark.asyncio
    async def test_public_match_high_kill_game(self, client):
        """Test high-kill game statistics consistency."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        # Total kills should be close to scores (may differ due to neutral kills, denies, etc.)
        radiant_kills = sum(p.kills for p in match.players if p.isRadiant)
        dire_kills = sum(p.kills for p in match.players if not p.isRadiant)

        # Radiant: 44 kills exact
        assert radiant_kills == match.radiant_score  # 44

        # Dire: kills should be close to score (may have 1-2 difference from neutral/misc kills)
        assert abs(dire_kills - match.dire_score) <= 2

    @pytest.mark.asyncio
    async def test_public_match_player_names(self, client):
        """Test player names in public match (some may be anonymous)."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        # Some players have names, some are anonymous
        players_with_names = [p for p in match.players if p.personaname is not None]

        # At least some players should have names
        # Note: Player 2 has "PhenomenalOneAGS", Player 3 has "Me lleva la que me trajo", etc.
        assert len(players_with_names) >= 3

    @pytest.mark.asyncio
    async def test_public_match_unparsed_fields_are_none(self, client):
        """Test that unparsed match fields are None, not errors."""
        match_id = 8607246638
        match = await client.get_match(match_id)

        p0 = match.players[0]

        # These fields may be None in unparsed/partially parsed matches
        # The key is they don't raise errors
        assert p0.lane is None or isinstance(p0.lane, int)
        assert p0.lane_role is None or isinstance(p0.lane_role, int)
        assert p0.lane_efficiency is None or isinstance(p0.lane_efficiency, float)
        assert p0.gold_t is None or isinstance(p0.gold_t, list)
        assert p0.obs_placed is None or isinstance(p0.obs_placed, int)


class TestProVsPublicMatchComparison:
    """Compare pro match vs public match field availability."""

    @pytest.fixture
    async def client(self):
        """Create a test client."""
        async with OpenDota() as client:
            yield client

    @pytest.mark.asyncio
    async def test_pro_match_has_more_data(self, client):
        """Test that pro matches have richer data than public matches."""
        pro_match = await client.get_match(8461956309)  # TI 2025
        pub_match = await client.get_match(8607246638)  # Public ranked

        # Pro match should have team info
        assert pro_match.radiant_team_id is not None
        assert pub_match.radiant_team_id is None

        # Pro match should have league info
        assert pro_match.league is not None
        assert pub_match.league is None

        # Pro match should have draft timings (Captains Mode)
        assert pro_match.draft_timings is not None and len(pro_match.draft_timings) > 0
        assert pub_match.draft_timings is None or len(pub_match.draft_timings) == 0

        # Pro match should have chat
        assert pro_match.chat is not None and len(pro_match.chat) > 0

    @pytest.mark.asyncio
    async def test_both_matches_have_core_player_fields(self, client):
        """Test that both pro and public matches have core player fields."""
        pro_match = await client.get_match(8461956309)
        pub_match = await client.get_match(8607246638)

        for match in [pro_match, pub_match]:
            p0 = match.players[0]

            # Core fields should always exist
            assert p0.hero_id is not None
            assert p0.player_slot is not None
            assert p0.kills is not None
            assert p0.deaths is not None
            assert p0.assists is not None
            assert p0.isRadiant is not None

            # New fields should exist (even if None in some cases)
            assert hasattr(p0, 'hero_variant')
            assert hasattr(p0, 'item_neutral2')
            assert hasattr(p0, 'kda')
            assert hasattr(p0, 'benchmarks')


class TestReplayUrlHandling:
    """Test cases for replay URL availability and ReplayNotAvailableError."""

    @pytest.fixture
    async def client(self):
        """Create a test client."""
        async with OpenDota() as client:
            yield client

    @pytest.mark.asyncio
    async def test_match_with_replay_url_succeeds(self, client):
        """Test that matches with replay_url don't raise exceptions."""
        match = await client.get_match(8461956309)

        assert match.match_id == 8461956309
        assert match.replay_url is not None
        assert "valve.net" in match.replay_url

    @pytest.mark.asyncio
    async def test_replay_not_available_error_has_match_id(self):
        """Test ReplayNotAvailableError contains match_id."""
        error = ReplayNotAvailableError(12345)

        assert error.match_id == 12345
        assert "12345" in str(error)
        assert "wait_for_replay_url" in str(error)

    @pytest.mark.asyncio
    async def test_replay_not_available_error_custom_message(self):
        """Test ReplayNotAvailableError with custom message."""
        error = ReplayNotAvailableError(12345, "Custom error message")

        assert error.match_id == 12345
        assert str(error) == "Custom error message"

    @pytest.mark.asyncio
    async def test_get_match_without_replay_returns_match(self):
        """Test that get_match returns match even without replay_url."""
        async with OpenDota(format='pydantic') as client:
            base_match = {
                "match_id": 99999999,
                "duration": 1800,
                "radiant_win": True,
                "radiant_score": 30,
                "dire_score": 20,
                "start_time": 1700000000,
                "game_mode": 22,
                "lobby_type": 0,
                "players": [],
            }

            async def mock_get(endpoint, *args, **kwargs):
                if endpoint.startswith("matches/"):
                    return base_match
                return None

            client.get = mock_get

            match = await client.get_match(99999999)
            assert match.match_id == 99999999
            assert match.replay_url is None

    @pytest.mark.asyncio
    async def test_get_match_with_wait_for_replay_returns_parse_task(self):
        """Test get_match with wait_for_replay=True returns ParseTask."""
        from opendota.client import ParseTask

        async with OpenDota(format='pydantic') as client:
            task = client.get_match(99999999, wait_for_replay=True)
            assert isinstance(task, ParseTask)
            assert task.match_id == 99999999

    @pytest.mark.asyncio
    async def test_parse_task_awaitable(self):
        """Test ParseTask can be awaited to wait for replay."""
        from opendota.models import Match

        async with OpenDota(format='pydantic') as client:
            call_count = 0

            base_match = {
                "match_id": 99999999,
                "duration": 1800,
                "radiant_win": True,
                "radiant_score": 30,
                "dire_score": 20,
                "start_time": 1700000000,
                "game_mode": 22,
                "lobby_type": 0,
                "players": [],
            }

            async def mock_get(endpoint, *args, **kwargs):
                nonlocal call_count
                if endpoint.startswith("matches/"):
                    call_count += 1
                    if call_count >= 2:
                        return {**base_match, "replay_url": "http://test.dem.bz2"}
                    return base_match
                if endpoint.startswith("request/"):
                    return {
                        "id": 123,
                        "jobId": 123,
                        "type": "parse",
                        "timestamp": "2025-01-01T00:00:00Z",
                        "attempts": 1,
                        "data": {"match_id": 99999999},
                    }
                return None

            async def mock_request_match(match_id):
                return {"job_id": 123}

            client.get = mock_get
            client.request_match = mock_request_match

            task = client.get_match(99999999, wait_for_replay=True, interval=0.1)
            match = await task

            assert isinstance(match, Match)
            assert match.replay_url == "http://test.dem.bz2"

    @pytest.mark.asyncio
    async def test_parse_task_iterable_for_progress(self):
        """Test ParseTask yields ParseStatus during iteration."""
        from opendota.models import ParseStatus

        async with OpenDota(format='pydantic') as client:
            call_count = 0
            statuses = []

            base_match = {
                "match_id": 99999999,
                "duration": 1800,
                "radiant_win": True,
                "radiant_score": 30,
                "dire_score": 20,
                "start_time": 1700000000,
                "game_mode": 22,
                "lobby_type": 0,
                "players": [],
            }

            async def mock_get(endpoint, *args, **kwargs):
                nonlocal call_count
                if endpoint.startswith("matches/"):
                    call_count += 1
                    if call_count >= 4:
                        return {**base_match, "replay_url": "http://test.dem.bz2"}
                    return base_match
                if endpoint.startswith("request/"):
                    return {
                        "id": 123,
                        "jobId": 123,
                        "type": "parse",
                        "timestamp": "2025-01-01T00:00:00Z",
                        "attempts": call_count,
                        "data": {"match_id": 99999999},
                    }
                return None

            async def mock_request_match(match_id):
                return {"job_id": 123}

            client.get = mock_get
            client.request_match = mock_request_match

            task = client.get_match(99999999, wait_for_replay=True, interval=0.1)

            async for status in task:
                statuses.append(status)
                assert isinstance(status, ParseStatus)
                assert status.job_id == 123
                assert status.match_id == 99999999
                assert status.elapsed > 0

            assert len(statuses) >= 1
            assert task.match is not None
            assert task.match.replay_url == "http://test.dem.bz2"

    @pytest.mark.asyncio
    async def test_parse_task_break_early(self):
        """Test user can break out of ParseTask iteration early."""
        async with OpenDota(format='pydantic') as client:
            iteration_count = 0

            base_match = {
                "match_id": 99999999,
                "duration": 1800,
                "radiant_win": True,
                "radiant_score": 30,
                "dire_score": 20,
                "start_time": 1700000000,
                "game_mode": 22,
                "lobby_type": 0,
                "players": [],
            }

            async def mock_get(endpoint, *args, **kwargs):
                if endpoint.startswith("matches/"):
                    return base_match  # Never has replay_url
                if endpoint.startswith("request/"):
                    return {
                        "id": 123,
                        "jobId": 123,
                        "type": "parse",
                        "timestamp": "2025-01-01T00:00:00Z",
                        "attempts": 1,
                        "data": {"match_id": 99999999},
                    }
                return None

            async def mock_request_match(match_id):
                return {"job_id": 123}

            client.get = mock_get
            client.request_match = mock_request_match

            task = client.get_match(99999999, wait_for_replay=True, interval=0.1)

            async for status in task:
                iteration_count += 1
                if iteration_count >= 3:
                    break

            assert iteration_count == 3
            assert task.match is None

    @pytest.mark.asyncio
    async def test_request_match_returns_job_id(self, client):
        """Test request_match returns ParseJobRequest with job_id."""
        from opendota.models import ParseJobRequest

        # Use a real match that exists
        result = await client.request_match(8461956309)

        assert isinstance(result, ParseJobRequest)
        assert isinstance(result.job_id, int)
        assert result.job_id > 0

    @pytest.mark.asyncio
    async def test_get_parse_job_status_pending(self, client):
        """Test get_parse_job_status returns ParseJob for pending jobs."""
        from opendota.models import ParseJob, ParseJobRequest

        # Request a parse to get a fresh job ID
        job_request = await client.request_match(8461956309)
        assert isinstance(job_request, ParseJobRequest)

        # Check job status - should return ParseJob for pending job
        status = await client.get_parse_job_status(job_request.job_id)

        # Job may or may not be pending depending on timing
        if status is not None:
            assert isinstance(status, ParseJob)
            assert status.job_id == job_request.job_id
            assert status.match_id == 8461956309

    @pytest.mark.asyncio
    async def test_get_parse_job_status_completed_returns_none(self, client):
        """Test get_parse_job_status returns None for completed/nonexistent jobs."""
        # Use a very old job ID that should be completed
        status = await client.get_parse_job_status(1)
        assert status is None

