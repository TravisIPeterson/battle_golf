import json
from models import Team

def save_teams(teams, filename="teams.json"):
    with open(filename, 'w') as file:
        json_data = [team.to_json() for team in teams]
        json.dump(json_data, file)

def load_teams(filename="teams.json"):
    with open(filename, 'r') as file:
        json_data = json.load(file)
        return [Team.from_json(team_data) for team_data in json_data]
