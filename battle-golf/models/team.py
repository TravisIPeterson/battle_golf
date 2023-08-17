import json
from .players.player_base import Player

class Team:
    def __init__(self, team_name, players=None):
        self.team_name = team_name
        default_roles = ['Driver', 'Blocker', 'Marksman', 'Goalie']
        if players:
            self.players = players
        else:
            self.players = {role: Player(role, green_number=int(self.team_name), team_name=self.team_name) for role in default_roles}

    def display_team(self):
        print(f"Team: {self.team_name}")
        for player_role, player in self.players.items():
            player.display_stats()
            print("-" * 40)

    def to_json(self):
        return {
            'team_name': self.team_name,
            'players': {
                role: player.stats for role, player in self.players.items()
            }
        }

    @classmethod
    def from_json(cls, data):
        players = {role: Player(role, stats) for role, stats in data['players'].items()}
        return cls(data['team_name'], players)


def save_teams(teams, filename="teams.json"):
    with open(filename, 'w') as file:
        json_data = [team.to_json() for team in teams]
        json.dump(json_data, file)


def load_teams(filename="teams.json"):
    with open(filename, 'r') as file:
        json_data = json.load(file)
        return [Team.from_json(team_data) for team_data in json_data]