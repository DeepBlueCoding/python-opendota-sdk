# Examples

??? info "🤖 AI Summary"

    Code examples for common tasks: **Match analysis** - get KDA, GPM, winner. **Player tracking** - profile, recent matches, winrate, most played heroes. **Meta heroes** - filter by pro pick rates, sort by win rate. **Player comparison** - compare stats between two players. **Pro match monitor** - poll for new pro matches. **Batch collection** - paginate through high MMR matches with rate limiting. **New in 7.40**: Draft analysis, support stats (wards, stacking), laning efficiency, gold/XP timelines, hero variants, comeback detection.

## Analyze Match Performance

```python
from opendota import OpenDota

async def analyze_match(match_id: int):
    async with OpenDota() as client:
        match = await client.get_match(match_id)

        print(f"Match {match_id} Analysis:")
        print(f"Duration: {match.duration // 60}m {match.duration % 60}s")
        print(f"Winner: {'Radiant' if match.radiant_win else 'Dire'}")
        print(f"Score: {match.radiant_score} - {match.dire_score}")

        # Find MVP by KDA
        best_kda = max(
            match.players,
            key=lambda p: (p.kills + p.assists) / max(p.deaths, 1)
        )
        team = "Radiant" if best_kda.player_slot < 128 else "Dire"
        print(f"Best KDA: {best_kda.kills}/{best_kda.deaths}/{best_kda.assists} ({team})")

        # Team gold comparison
        radiant_gpm = sum(p.gold_per_min for p in match.players if p.player_slot < 128)
        dire_gpm = sum(p.gold_per_min for p in match.players if p.player_slot >= 128)
        print(f"Avg GPM - Radiant: {radiant_gpm/5:.0f}, Dire: {dire_gpm/5:.0f}")
```

## Track Player Progress

```python
from opendota import OpenDota

async def track_player(account_id: int):
    async with OpenDota() as client:
        # Get player profile
        player = await client.get_player(account_id)
        print(f"Player: {player.profile.personaname}")
        print(f"Rank: {player.rank_tier}")

        # Get recent matches
        matches = await client.get_player_matches(account_id, limit=20)

        wins = sum(1 for m in matches if (m.player_slot < 128) == m.radiant_win)
        total = len(matches)
        winrate = wins / total * 100

        avg_kills = sum(m.kills for m in matches) / total
        avg_deaths = sum(m.deaths for m in matches) / total
        avg_assists = sum(m.assists for m in matches) / total

        print(f"Last {total} matches:")
        print(f"Winrate: {winrate:.1f}% ({wins}/{total})")
        print(f"Avg KDA: {avg_kills:.1f}/{avg_deaths:.1f}/{avg_assists:.1f}")

        # Most played heroes
        hero_counts = {}
        for match in matches:
            hero_counts[match.hero_id] = hero_counts.get(match.hero_id, 0) + 1

        heroes = await client.get_heroes()
        hero_names = {h.id: h.localized_name for h in heroes}

        print("Most played heroes:")
        for hero_id, count in sorted(hero_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"  {hero_names.get(hero_id, 'Unknown')}: {count} games")
```

## Find Meta Heroes

```python
from opendota import OpenDota

async def find_meta_heroes():
    async with OpenDota() as client:
        hero_stats = await client.get_hero_stats()

        # Filter heroes with significant pick rates
        meta_heroes = [h for h in hero_stats if (h.pro_pick or 0) > 50]

        # Sort by win rate
        meta_heroes.sort(
            key=lambda h: (h.pro_win or 0) / max(h.pro_pick or 1, 1),
            reverse=True
        )

        print("Current meta heroes (high pick + win rate):")
        for hero in meta_heroes[:10]:
            if hero.pro_pick and hero.pro_win:
                winrate = hero.pro_win / hero.pro_pick * 100
                print(f"{hero.localized_name}: {winrate:.1f}% WR ({hero.pro_pick} picks)")
```

## Compare Two Players

```python
from opendota import OpenDota

async def compare_players(player1_id: int, player2_id: int):
    async with OpenDota() as client:
        p1 = await client.get_player(player1_id)
        p2 = await client.get_player(player2_id)

        p1_matches = await client.get_player_matches(player1_id, limit=50)
        p2_matches = await client.get_player_matches(player2_id, limit=50)

        def calc_stats(matches):
            wins = sum(1 for m in matches if (m.player_slot < 128) == m.radiant_win)
            avg_kda = sum(m.kills + m.assists for m in matches) / max(sum(m.deaths for m in matches), 1)
            return {"winrate": wins / len(matches) * 100, "kda": avg_kda}

        stats1 = calc_stats(p1_matches)
        stats2 = calc_stats(p2_matches)

        print(f"Comparison: {p1.profile.personaname} vs {p2.profile.personaname}")
        print(f"Winrate: {stats1['winrate']:.1f}% vs {stats2['winrate']:.1f}%")
        print(f"Avg KDA: {stats1['kda']:.2f} vs {stats2['kda']:.2f}")
```

## Pro Match Monitor

```python
from opendota import OpenDota
import asyncio

async def monitor_pro_matches():
    async with OpenDota() as client:
        last_match_id = None

        while True:
            pro_matches = await client.get_pro_matches()

            for match in pro_matches:
                if last_match_id and match.match_id <= last_match_id:
                    break

                if match.radiant_name and match.dire_name:
                    winner = match.radiant_name if match.radiant_win else match.dire_name
                    print(f"[{match.league_name}] {match.radiant_name} vs {match.dire_name}")
                    print(f"  Winner: {winner} ({match.duration // 60}m)")

            if pro_matches:
                last_match_id = pro_matches[0].match_id

            await asyncio.sleep(60)  # Check every minute
```

## Batch Data Collection

```python
from opendota import OpenDota
import asyncio

async def collect_high_mmr_matches(count: int = 100):
    async with OpenDota() as client:
        all_matches = []
        last_match_id = None

        while len(all_matches) < count:
            matches = await client.get_public_matches(
                mmr_descending=6000,
                less_than_match_id=last_match_id
            )

            if not matches:
                break

            all_matches.extend(matches)
            last_match_id = matches[-1].match_id

            # Respect rate limits
            await asyncio.sleep(1)

        print(f"Collected {len(all_matches)} high MMR matches")
        return all_matches[:count]
```

## Analyze Pro Match Draft (New in 7.40)

```python
from opendota import OpenDota

async def analyze_draft(match_id: int):
    async with OpenDota() as client:
        match = await client.get_match(match_id)

        if not match.draft_timings:
            print("No draft data (not Captains Mode)")
            return

        # Get hero names
        heroes = await client.get_heroes()
        hero_names = {h.id: h.localized_name for h in heroes}

        print(f"Draft: {match.radiant_name} vs {match.dire_name}")
        print(f"Tournament: {match.league.name}\n")

        bans = [d for d in match.draft_timings if not d.pick]
        picks = [d for d in match.draft_timings if d.pick]

        print("Bans:")
        for ban in bans:
            team = match.radiant_name if ban.active_team == 0 else match.dire_name
            hero = hero_names.get(ban.hero_id, "Unknown")
            print(f"  {team}: {hero}")

        print("\nPicks:")
        for pick in picks:
            team = match.radiant_name if pick.active_team == 0 else match.dire_name
            hero = hero_names.get(pick.hero_id, "Unknown")
            print(f"  {team}: {hero}")
```

## Support Player Analysis (New in 7.40)

```python
from opendota import OpenDota

async def analyze_supports(match_id: int):
    async with OpenDota() as client:
        match = await client.get_match(match_id)
        heroes = await client.get_heroes()
        hero_names = {h.id: h.localized_name for h in heroes}

        print(f"Support Analysis: {match.radiant_name} vs {match.dire_name}\n")

        # Find supports by ward placement
        supports = sorted(
            match.players,
            key=lambda p: (p.obs_placed or 0) + (p.sen_placed or 0),
            reverse=True
        )[:4]  # Top 4 ward placers

        for player in supports:
            team = "Radiant" if player.isRadiant else "Dire"
            hero = hero_names.get(player.hero_id, "Unknown")

            print(f"[{team}] {player.personaname} - {hero}")
            print(f"  Wards: {player.obs_placed or 0} obs, {player.sen_placed or 0} sen")
            print(f"  Camps stacked: {player.camps_stacked or 0}")
            print(f"  Teamfight: {(player.teamfight_participation or 0) * 100:.0f}%")
            print()
```

## Laning Phase Analysis (New in 7.40)

```python
from opendota import OpenDota

async def analyze_laning(match_id: int):
    async with OpenDota() as client:
        match = await client.get_match(match_id)
        heroes = await client.get_heroes()
        hero_names = {h.id: h.localized_name for h in heroes}

        lane_names = {1: "Safelane", 2: "Mid", 3: "Offlane"}

        print("Laning Phase Analysis\n")

        for team_name, is_radiant in [("Radiant", True), ("Dire", False)]:
            print(f"{team_name}:")
            team_players = [p for p in match.players if p.isRadiant == is_radiant]

            for player in sorted(team_players, key=lambda p: p.lane or 0):
                hero = hero_names.get(player.hero_id, "Unknown")
                lane = lane_names.get(player.lane, "Unknown")
                eff = (player.lane_efficiency or 0) * 100

                print(f"  {hero} ({lane}): {eff:.0f}% efficiency")

            print()
```

## Gold/XP Timeline (New in 7.40)

```python
from opendota import OpenDota

async def plot_economy(match_id: int):
    async with OpenDota() as client:
        match = await client.get_match(match_id)

        # Get carry players (highest GPM)
        carries = sorted(match.players, key=lambda p: p.gold_per_min, reverse=True)[:2]

        for player in carries:
            if not player.gold_t:
                continue

            team = "Radiant" if player.isRadiant else "Dire"
            print(f"[{team}] {player.personaname}")
            print(f"  Final gold: {player.gold_t[-1]:,}")
            print(f"  10 min gold: {player.gold_t[10]:,}")
            print(f"  20 min gold: {player.gold_t[20]:,}")

            # Calculate gold gained per phase
            laning = player.gold_t[10] - player.gold_t[0]
            mid = player.gold_t[20] - player.gold_t[10]
            late = player.gold_t[-1] - player.gold_t[20]

            print(f"  Laning (0-10): +{laning:,}")
            print(f"  Mid (10-20): +{mid:,}")
            print(f"  Late (20+): +{late:,}")
            print()
```

## Hero Variant Tracking (New in 7.40)

```python
from opendota import OpenDota

async def find_arcana_games(hero_id: int, limit: int = 100):
    """Find recent games where players used hero personas/arcanas."""
    async with OpenDota() as client:
        heroes = await client.get_heroes()
        hero_name = next((h.localized_name for h in heroes if h.id == hero_id), "Unknown")

        matches = await client.get_public_matches()
        arcana_count = 0

        for pub_match in matches[:limit]:
            match = await client.get_match(pub_match.match_id)

            for player in match.players:
                if player.hero_id == hero_id and player.hero_variant and player.hero_variant > 0:
                    arcana_count += 1
                    print(f"Match {match.match_id}: {hero_name} variant {player.hero_variant}")

        print(f"\nFound {arcana_count} games with {hero_name} arcana/persona")
```

## Match Comeback Detection (New in 7.40)

```python
from opendota import OpenDota

async def find_comebacks():
    async with OpenDota() as client:
        pro_matches = await client.get_pro_matches()

        comebacks = []
        for pm in pro_matches[:20]:
            match = await client.get_match(pm.match_id)

            if match.comeback and match.comeback > 1000:
                comebacks.append({
                    "match_id": match.match_id,
                    "teams": f"{match.radiant_name} vs {match.dire_name}",
                    "comeback": match.comeback,
                    "winner": match.radiant_name if match.radiant_win else match.dire_name
                })

        print("Recent Comeback Games:")
        for game in sorted(comebacks, key=lambda x: x["comeback"], reverse=True):
            print(f"  {game['teams']}")
            print(f"    Comeback score: {game['comeback']:.0f}")
            print(f"    Winner: {game['winner']}")
            print()
```
