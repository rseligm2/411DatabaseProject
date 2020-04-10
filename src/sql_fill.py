import sqlite3 as sql
import json
import jsonpickle

from src.config import SQL_DB_FILE
from src.calls import get_team

connection = sql.connect(str(SQL_DB_FILE))
cursor = connection.cursor()


def insert_team(team_id):
    raw_data = get_team(team_id)
    data = jsonpickle.decode(raw_data)
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


insert_team(33)

# cursor.execute("SELECT * FROM Teams")
# print("fetchall:")
# result = cursor.fetchall()
# for r in result:
#     print(r)
