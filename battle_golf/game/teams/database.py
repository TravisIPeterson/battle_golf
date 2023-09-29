import sqlite3
from game.teams.player import Player
from game.teams.team import Team

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS players
                            (name TEXT, position TEXT, power REAL, accuracy REAL, speed REAL,
                             visual_calculus REAL, balance REAL, solidity REAL, savagery REAL,
                             competitiveness REAL, cowardice REAL, neoliberalism REAL,
                             integrity REAL, goutiness REAL, team_id INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS teams
                            (id INTEGER PRIMARY KEY, name TEXT)''')
        self.conn.commit()

    def insert_player(self, player, team_id):
        self.cursor.execute('''INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (player.name, player.position, player.stats['Power'], player.stats['Accuracy'],
                             player.stats['Speed'], player.stats['Visual Calculus'], player.stats['Balance'],
                             player.stats['Solidity'], player.stats['Savagery'], player.stats['Competitiveness'],
                             player.stats['Cowardice'], player.stats['Neoliberalism'], player.stats['Integrity'],
                             player.stats['Goutiness'], team_id))
        self.conn.commit()

    def insert_team(self, team):
        self.cursor.execute('''INSERT INTO teams (name) VALUES (?)''', (team.name,))
        team_id = self.cursor.lastrowid
        for player in team.players:
            self.insert_player(player, team_id)
        self.conn.commit()

    def get_teams(self):
        self.cursor.execute("SELECT * FROM teams")
        rows = self.cursor.fetchall()
        teams = []
        for row in rows:
            team_id = row[0]
            team_name = row[1]
            players = self.get_players_by_team(team_id)
            teams.append(Team(team_name, players))
        return teams

    def get_players_by_team(self, team_id):
        self.cursor.execute("SELECT * FROM players WHERE team_id=?", (team_id,))
        rows = self.cursor.fetchall()
        players = []
        for row in rows:
            stats = {
                'Power': row[2],
                'Accuracy': row[3],
                'Speed': row[4],
                'Visual Calculus': row[5],
                'Balance': row[6],
                'Solidity': row[7],
                'Savagery': row[8],
                'Competitiveness': row[9],
                'Cowardice': row[10],
                'Neoliberalism': row[11],
                'Integrity': row[12],
                'Goutiness': row[13]
            }
            players.append(Player(row[0], row[1], stats))
        return players