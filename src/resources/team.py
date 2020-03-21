from dataclasses import *
from typing import *

@dataclass
class Team:
    team_id: int
    name: str
    code: Optional[Any]
    logo: str
    is_national: bool
    country: str
    founded: int
    venue_name: str
    venue_surface: str
    venue_address: str
    venue_city: str
    venue_capacity: int


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

{
    "api": {
        "results": 3,
        "players": [
            {
                "player_id": 276,
                "player_name": "Neymar da Silva Santos Junior",
                "firstname": "Neymar",
                "lastname": "da Silva Santos Junior",
                "number": 10,
                "position": "Attacker",
                "age": 27,
                "birth_date": "05/02/1992",
                "birth_place": "Mogi das Cruzes",
                "birth_country": "Brazil",
                "nationality": "Brazil",
                "height": "175 cm",
                "weight": "68 kg",
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
    }
}
"""