import sqlite3 as sql
import json

from src.config import SQL_DB_FILE
from src.calls import get_team

connection = sql.connect(str(SQL_DB_FILE))
cursor = connection.cursor()


def insert_team(team):
    # raw_data = get_team(team_id)
    # raw_data = '{"api":{"results":1,"teams":[{"team_id":33,"name":"Manchester United","code":"MUN","logo":"https:\/\/media.api-sports.io\/teams\/33.png","country":"England","is_national":false,"founded":1878,"venue_name":"Old Trafford","venue_surface":"grass","venue_address":"Sir Matt Busby Way","venue_city":"Manchester","venue_capacity":76212}]}}'
    # print(raw_data)
    # data = json.loads(raw_data)
    # team = data["api"]["teams"][0]
    format_str = """INSERT INTO Teams (
        team_id,
        name,
        logo,
        is_national,
        country,
        founded,
        venue_name,
        venue_surface,
        venue_address,
        venue_city,
        venue_capacity)
        VALUES ( "{team_id}", "{name}", "{logo}", "{is_national}", "{country}", "{founded}", "{venue_name}", "{venue_surface}", "{venue_address}", "{venue_city}", "{venue_capacity}");"""
    command = format_str.format(
        team_id=team["team_id"],
        name=team["name"],
        logo=team["logo"],
        is_national=team["is_national"],
        country=team["country"],
        founded=team["founded"],
        venue_name=team["venue_name"],
        venue_surface=team["venue_surface"],
        venue_address=team["venue_address"],
        venue_city=team["venue_city"],
        venue_capacity=team["venue_capacity"]
    )
    try:
        cursor.execute(command)
    except sql.IntegrityError:
        print("team_id not unique: ")
    connection.commit()
    #cursor.close()


def insert_player(player):
    """Input individual player object into db:
        example:

        players = data["api"]["players"]
        for player in players:
            insert_player(player)"""
    format_str = """INSERT INTO Players (
            player_id,
            player_name,
            firstname,
            lastname,
            number,
            position,
            age,
            birth_date,
            birth_place,
            birth_country,
            nationality,
            height,
            weight)
            VALUES ( "{player_id}", "{player_name}", "{firstname}", "{lastname}", "{number}", "{position}", "{age}", "{birth_date}", "{birth_place}", "{birth_country}", "{nationality}", "{height}", "{weight}");"""
    command = format_str.format(
        player_id=player["player_id"],
        player_name=player["player_name"],
        firstname=player["firstname"],
        lastname=player["lastname"],
        number=player["number"],
        position=player["position"],
        age=player["age"],
        birth_date=player["birth_date"],
        birth_place=player["birth_place"],
        birth_country=player["birth_country"],
        nationality=player["nationality"],
        height=player["height"],
        weight=player["weight"]
    )
    try:
        cursor.execute(command)
    except sql.IntegrityError:
        print("player_id not unique: ")

    connection.commit()


def insert_player_stats(player):
    """Input individual player object into db:
        example:

        players = data["api"]["players"]
        for player in players:
            insert_player_stats(player)"""
    format_str = """INSERT INTO PlayerStats (
            player_id,
            injured,
            rating,
            team_id,
            team_name,
            league,
            season,
            captain,
            shots_total,
            shots_on,
            goals_total,
            goals_conceded,
            goals_assists,
            passes_total,
            passes_key, 
            passes_accuracy,
            tackles_total,
            tackles_blocks,
            tackles_interceptions,
            duels_total,
            duels_won,
            dribbles_attempts,
            dribbles_success,
            fouls_draw,
            fouls_committed,
            cards_yellow,
            cards_yellowred,
            cards_red,
            penalty_won,
            penalty_commited,
            penalty_success,
            penalty_missed,
            penalty_saved,
            games_appearances,
            games_minutes_played,
            games_lineups,
            substitutes_in,
            substitutes_out,
            substitutes_bench)
            VALUES ("{player_id}", "{injured}", "{rating}", "{team_id}", "{team_name}", "{league}", "{season}", "{captain}", "{shots_total}", "{shots_on}", "{goals_total}", "{goals_conceded}", "{goals_assists}", "{passes_key}", "{passes_total}", "{passes_accuracy}", "{tackles_total}", "{tackles_blocks}", "{tackles_interceptions}", "{duels_total}", "{duels_won}", "{dribbles_attempts}", "{dribbles_success}", "{fouls_draw}", "{fouls_committed}", "{cards_yellow}", "{cards_yellowred}", "{cards_red}", "{penalty_won}", "{penalty_commited}", "{penalty_success}", "{penalty_missed}", "{penalty_saved}", "{games_appearances}", "{games_minutes_played}", "{games_lineups}", "{substitutes_in}", "{substitutes_out}", "{substitutes_bench}");"""
    command = format_str.format(
        player_id=player["player_id"],
        injured=player["injured"],
        rating=player["rating"],
        team_id=player["team_id"],
        team_name=player["team_name"],
        league=player["league"],
        season=player["season"],
        captain=player["captain"],

        shots_total=player["shots"]["total"],
        shots_on=player["shots"]["on"],

        goals_total=player["goals"]["total"],
        goals_conceded=player["goals"]["conceded"],
        goals_assists=player["goals"]["assists"],

        passes_key=0,
        passes_total=player["passes"]["total"],
        passes_accuracy=player["passes"]["accuracy"],

        tackles_total=player["tackles"]["total"],
        tackles_blocks=player["tackles"]["blocks"],
        tackles_interceptions=player["tackles"]["interceptions"],

        duels_total=player["duels"]["total"],
        duels_won=player["duels"]["won"],

        dribbles_attempts=player["dribbles"]["attempts"],
        dribbles_success=player["dribbles"]["success"],

        fouls_draw=player["fouls"]["drawn"],
        fouls_committed=player["fouls"]["committed"],

        cards_yellow=player["cards"]["yellow"],
        cards_yellowred=player["cards"]["yellowred"],
        cards_red=player["cards"]["red"],

        penalty_success=player["penalty"]["success"],
        penalty_missed=player["penalty"]["missed"],
        penalty_saved=player["penalty"]["saved"],
        penalty_won=player["penalty"]["won"],
        penalty_commited=player["penalty"]["commited"],

        games_appearances=player["games"]["appearences"],
        games_minutes_played=player["games"]["minutes_played"],
        games_lineups=player["games"]["lineups"],

        substitutes_in=player["substitutes"]["in"],
        substitutes_out=player["substitutes"]["out"],
        substitutes_bench=player["substitutes"]["bench"]
    )
    try:
        cursor.execute(command)
    except sql.IntegrityError:
        print("player_id not unique: ")

    connection.commit()

# insert_team(33)

query = """

SELECT A_name, B_name, AVG(Sim) AS Sim
FROM
(
SELECT A_name, B_name, (CAST(ABS(A_cap - B_cap) AS float) / CAST(A_cap AS float)) AS Sim FROM

(SELECT A.name AS A_name, B.name AS B_name, A.venue_capacity AS A_cap, B.venue_capacity AS B_cap 
FROM Teams A, Teams B
WHERE A.team_id <> B.team_id AND A.venue_surface = B.venue_surface)

ORDER BY (CAST(ABS(A_cap - B_cap) AS float) / CAST(A_cap AS float))
)
GROUP BY A_name

ORDER BY Sim DESC
"""

print(list(cursor.execute(query)))
connection.commit()

# cursor.execute("SELECT * FROM Teams")
# print("fetchall:")
# result = cursor.fetchall()
# for r in result:
#     print(r)
