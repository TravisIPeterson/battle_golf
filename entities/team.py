import sqlite3
from entities.player import Player

class Team:
    def __init__(self, id, name, players):
        self.id = id
        self.name = name
        self.players = players
        self.score = 0

    @staticmethod
    def get_teams_from_db(database):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM teams')
        teams_data = cursor.fetchall()

        # Retrieve all players using the Player class method
        # This assumes that get_players_from_db is a static method of the Player class
        players = Player.get_players_from_db()

        # Create a dictionary to hold teams
        teams = {team_id: Team(id=team_id, name=team_name, players=[]) for team_id, team_name in teams_data}

        # Assign players to their respective teams
        for player in players:
            # Make sure player.team_id is an integer if team_id from teams_data is an integer
            player_team_id = int(player.team_id) if isinstance(player.team_id, str) else player.team_id
            if player_team_id in teams:
                teams[player_team_id].players.append(player)
        
        conn.close()

        # Return the list of team objects
        return list(teams.values())
