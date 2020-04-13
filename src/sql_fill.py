import sqlite3 as sql
import json

from src.config import SQL_DB_FILE
from src.calls import get_team

connection = sql.connect(str(SQL_DB_FILE))
cursor = connection.cursor()


def insert_team(team_id):
    # raw_data = get_team(team_id)
    raw_data = '{"api":{"results":1,"teams":[{"team_id":33,"name":"Manchester United","code":"MUN","logo":"https:\/\/media.api-sports.io\/teams\/33.png","country":"England","is_national":false,"founded":1878,"venue_name":"Old Trafford","venue_surface":"grass","venue_address":"Sir Matt Busby Way","venue_city":"Manchester","venue_capacity":76212}]}}'
    # print(raw_data)
    data = json.loads(raw_data)
    team = data["api"]["teams"][0]
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
    cursor.execute(command)
    connection.commit()
    #cursor.close()


def insert_player(player):
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
