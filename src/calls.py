import requests
from src.app_secrets import headers

base_url = "https://api-football-v1.p.rapidapi.com/v2/"


def get_team(team_id):
    url = base_url + "teams/team/" + str(team_id)
    response = requests.request("GET", url, headers=headers)
    return response.text


def get_players_on_team(team_id):
    url = base_url + "players/team/" + str(team_id)
    response = requests.request("GET", url, headers=headers)
    return response.text

def get_teams_from_league(league_id):
    url = base_url + "teams/league/" + str(league_id)
    response = requests.request("GET", url, headers=headers)
    return response.text
