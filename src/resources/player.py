from dataclasses import *
from typing import *


"""
The Base component that fundamentally makes up who a player is belongs here.

The is the direct result of the Player Search API from:
https://www.api-football.com/documentation#players-search-response-model
"""


@dataclass
class PlayerBaseComponent:
    player_id: int
    player_name: str
    firstname: str
    lastname: str
    number: Optional[int]
    position: str
    age: int
    birth_date: str
    birth_place: str
    birth_country: str
    nationality: str
    height: str
    weight: str


"""
SQUAD API:
Params:
- {team_id} and {season}

Simplify it to just an array of player ids
"""


"""
Statistics API:

PARAMS:
player_id, team_id, season
        "players": [
            {
                "injured": "False",
                "rating": "8.183333",
                "team_id": 85,
                "team_name": "Paris Saint Germain",
                "league": "UEFA Champions League",
                "season": "2018-2019",
                "captain": 0,
                "shots": {
                    "total": 24,
                    "on": 16
                },
                "goals": {
                    "total": 5,
                    "conceded": 0,
                    "assists": 2
                },
                "passes": {
                    "total": 262,
                    "key": 0,
                    "accuracy": 82
                },
                "tackles": {
                    "total": 3,
                    "blocks": 2,
                    "interceptions": 2
                },
                "duels": {
                    "total": 122,
                    "won": 72
                },
                "dribbles": {
                    "attempts": 54,
                    "success": 32
                },
                "fouls": {
                    "drawn": 34,
                    "committed": 4
                },
                "cards": {
                    "yellow": 2,
                    "yellowred": 0,
                    "red": 0
                },
                "penalty": {
                    "won": 0,
                    "commited": 0,
                    "success": 0,
                    "missed": 0,
                    "saved": 0
                },
                "games": {
                    "appearences": 6,
                    "minutes_played": 532,
                    "lineups": 6
                },
                "substitutes": {
                    "in": 0,
                    "out": 1,
                    "bench": 0
                }
            },
        ]
"""


@dataclass
class PlayerStats:
    player_id: int
    injured: bool
    rating: float
    team_id: int
    team_name: str
    league: str
    season: str
    captain: str
    # Composite stats
    shots_total: int
    shots_on: int

    goals_total: int
    goals_conceded: int
    goals_assists: int

    passes_total: int
    passes_key: int
    passes_accuracy: float

    tackles_total: int
    tackles_blocks: int
    tackles_interceptions: int

    duels_total: int
    duels_won: int

    dribbles_attempts: int
    dribbles_success: int

    fouls_draw: int
    fouls_committed: int

    cards_yellow: int
    cards_yellowred: int
    cards_red: int

    penalty_won: int
    penalty_commited: int
    penalty_success: int
    penalty_missed: int
    penalty_saved: int

    games_appearances: int
    games_minutes_played: int
    games_lineups: int

    substitutes_in: int
    substitutes_out: int
    substitutes_bench: int
