import json

import requests

from src.sql import get_connection
from src.app_secrets import api_header
from src.resources.team import Team
from src.resources.player import PlayerBaseComponent
from src.resources.player import PlayerStats
def api_request(request):

    if request == 'countries':
        url = "https://api-football-v1.p.rapidapi.com/v2/countries"
    else:
        url = f"https://api-football-v1.p.rapidapi.com/v2/teams/search/{request}"

    req = requests.get(url, headers=api_header)
    if not req.content:
        return None

    return json.loads(req.content)

# TODO: Fix the interface of this function so that it is not absolutely awful
def load_from_database(request, request_type):
    #request_type = None
    if request_type == "countries":
        connection = get_connection()
        cursor = connection.cursor()
        iterable = cursor.execute(
            f"SELECT DISTINCT country FROM Teams"
        )
        connection.commit()
        rel = iterable.fetchall()
        return rel
    elif request_type == "teams_country":
        connection = get_connection()
        cursor = connection.cursor()

        iterable = cursor.execute(
            f"SELECT * FROM Teams WHERE country LIKE '{request}%'"
        )
        connection.commit()
        rel = iterable.fetchall()
        return rel
    else:
        # Currently other refers to teams
        # Note that we don't sanitize inputs because that is the requirement of the project
        # If you ever port this code to something in production, don't explicitly write queries
        # like this or else you will lose your job.
        connection = get_connection()
        cursor = connection.cursor()

        if request == "teams":

            iterable = cursor.execute(
                f"SELECT * FROM Teams"
            )
            connection.commit()

            rel = iterable.fetchall()

            return rel
        else:
            iterable = cursor.execute(
                f"SELECT * FROM Teams WHERE name LIKE '{request}%'"
            )
            connection.commit()

            rel = iterable.fetchone()
            #print(rel)
    team = Team(*rel)
            #print(team)

            # if not found return requests get ["api"]["teams"][0]
    return team


def load_all_players():
    conn = get_connection()
    cursor = conn.cursor()
    iterable = cursor.execute(
        f"SELECT * FROM Players NATURAL JOIN PlayerStats GROUP BY Players.player_id ORDER BY SUM(PlayerStats.games_minutes_played) DESC LIMIT 30"
    )
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in iterable.fetchall()]

    return result



def load_player_info(player):
    conn = get_connection()
    cursor = conn.cursor()
    iterable = cursor.execute(
        f"SELECT * FROM Players WHERE player_id='{player}'"
    )
    rel = iterable.fetchone()
    player_profile = PlayerBaseComponent(*rel)
    return player_profile


def player_stats_join(player):
    """Input player_id

        returns rows of Player and PlayerStats tables joined
    """
    conn = get_connection()
    cursor = conn.cursor()

    iterable = cursor.execute(
        f"SELECT * FROM Players NATURAL JOIN PlayerStats WHERE PlayerStats.player_id='{player}'"
    )
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in iterable.fetchall()]

    # rel = iterable.fetchall()

    return result

