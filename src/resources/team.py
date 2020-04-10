from dataclasses import *
from typing import *


@dataclass
class Team:
    team_id: int
    name: str
    # code: Optional[Any]
    logo: str
    is_national: bool
    country: str
    founded: int
    venue_name: str
    venue_surface: str
    venue_address: str
    venue_city: str
    venue_capacity: int


@dataclass
class Coach:
    coach_id: int
    name: str
    firstname: str
    lastname: str
    age: int
    birth_date: str
    birth_place: str
    birth_country: str
    nationality: str
    weight: Optional[int]
    height: Optional[int]


@dataclass
class CoachedFor:
    team_id: int
    coach_id: int
    season: str
    start_date: str
    end_date: str
