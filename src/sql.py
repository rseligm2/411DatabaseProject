import sqlite3 as sql
from dataclasses import asdict, astuple, dataclass, is_dataclass, make_dataclass
from typing import Any, Dict, List, Optional, Union

from src.config import SQL_DB_FILE


def get_connection():
    return sql.connect(str(SQL_DB_FILE))


@dataclass
class Table:
    init_command: str
    # schema: Dict[str, str] = {}


"""List of tables nicluding queries since the actual database queries need to be shown"""
_tables = {
    "Players": Table(
        """CREATE TABLE IF NOT EXISTS Players (
            player_id integer PRIMARY KEY,
            player_name text NOT NULL,
            firstname text,
            lastname text,
            number integer,
            position text,
            age integer,
            birth_date text,
            birth_place text,
            birth_country text,
            nationality text,
            height text,
            weight text
        );"""
    ),
    "Teams": Table(
        """CREATE TABLE IF NOT EXISTS Teams (
            team_id integer PRIMARY KEY,
            name text,
            logo text,
            is_national boolean,
            country text,
            founded date,
            venue_name text,
            venue_surface text,
            venue_address text,
            venue_city text,
            venue_capacity integer
        );
        """
    ),
    "PlayerStats": Table(
        """CREATE TABLE IF NOT EXISTS PlayerStats(
            player_id integer NOT NULL,
            injured boolean,
            rating float,
            team_id integer NOT NULL,
            team_name text,
            league text,
            season text NOT NULL,
            captain text,
    
            shots_total integer,
            shots_on integer,

            goals_total integer,
            goals_conceded integer,
            goals_assists integer,

            passes_total integer,
            passes_accuracy float,

            tackles_total integer,
            tackles_blocks integer,
            tackles_interceptions integer,

            duels_total integer,
            duels_won integer,

            dribbles_attempts integer,
            dribbles_success integer,

            fouls_draw integer,
            fouls_committed integer,
    
            cards_yellow integer,
            cards_yellowred integer,
            cards_red integer,
    
            penalty_success integer,
            penalty_missed integer,
            penalty_saved integer,

            games_appearances integer,
            games_minutes_played integer,
            games_lineups integer,

            substitutes_in integer,
            substitutes_out integer,
            substitutes_bench integer,

            FOREIGN KEY (player_id) REFERENCES Players(player_id),
            FOREIGN KEY (team_id) REFERENCES Teams(team_id),
            PRIMARY KEY (player_id, team_id, season)
        );
        """
    ),
    "Coaches": Table(
        """CREATE TABLE IF NOT EXISTS Coaches (
            coach_id integer PRIMARY KEY,
            name text,
            firstname text,
            lastname text,
            age integer,
            birth_date date,
            birth_place text,
            birth_country text,
            nationality text,
            weight integer,
            height integer
        );
        """
    ),
    "CoachedFor": Table(
        """CREATE TABLE IF NOT EXISTS CoachedFor (
            team_id integer NOT NULL,
            coach_id integer NOT NULL,
            season text NOT NULL,

            start_date text,
            end_date text,

            FOREIGN KEY (coach_id) REFERENCES Coaches(coach_id),
            FOREIGN KEY (team_id) REFERENCES Teams(team_id),
            PRIMARY KEY (coach_id, team_id, season)
        );
        """
    ),
}


def init_database():
    connection = get_connection()
    cursor = connection.cursor()
    [cursor.execute(com.init_command) for table_name, com in _tables.items()]
    connection.commit()


def get_player_names():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT player_name FROM Players")
    connection.commit()
    return [i[0] for i in cursor.fetchall()]


def get_team_names():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT name FROM Teams")
    connection.commit()
    return [i[0] for i in cursor.fetchall()]


def get_league_names():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT league FROM PlayerStats ORDER BY league")
    connection.commit()
    return [i[0] for i in cursor.fetchall()]


def advanced_search_teams(search_string, sort_by, league, team):
    base_query = f'''SELECT
                    DISTINCT Teams.name, PlayerStats.league, Teams.team_id
                FROM
                    Teams JOIN PlayerStats on Teams.team_id = PlayerStats.team_id
                WHERE
                    Teams.name LIKE "{search_string}%"
                '''

    if league != "":
        base_query += f'\tAND PlayerStats.league = "{league}"\n'

    if team != "":
        base_query += f'\tAND Teams.name = "{team}"\n'

    if sort_by.lower() == "country":
        base_query += f"ORDER BY Teams.{sort_by.lower()}"

    if sort_by.lower() == "league":
        base_query += f"ORDER BY PlayerStats.{sort_by.lower()}"

    print(base_query)

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        base_query
    )
    connection.commit()
    return cursor.fetchall()


def advanced_search_players(search_string, sort_by, league, team):
    base_query = f'''SELECT
                    DISTINCT Players.player_name, PlayerStats.league, Players.player_id
                FROM
                    Players JOIN PlayerStats on Players.player_id = PlayerStats.player_id
                WHERE
                    Players.player_name LIKE "{search_string}%"
                '''

    if league != "":
        base_query += f'\tAND PlayerStats.league = "{league}"\n'

    if team != "":
        base_query += f'\tAND PlayerStats.team_name = "{team}"\n'

    if sort_by.lower() == "country":
        base_query += f"ORDER BY Players.nationality"

    if sort_by.lower() == "league":
        base_query += f"ORDER BY PlayerStats.{sort_by.lower()}"

    print(base_query)

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        base_query
    )
    connection.commit()
    return cursor.fetchall()

init_database()
