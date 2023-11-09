import sqlite3
import sys
sys.path.append('..')
from entities.player import Player

team_names = {
    1: 'Toronto Trombones',
    2: 'Sioux City Sasquatches',
    3: 'Bermuda Barracudas',
    4: 'London Yankees',
    5: 'Berlin Hamburgers',
    6: 'Osaka Ocelots',
    7: 'Laguna Beach Creatures',
}

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('DROP TABLE IF EXISTS players')
        self.cursor.execute('DROP TABLE IF EXISTS teams')

        self.cursor.execute('''
            CREATE TABLE teams (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE players (
                id INTEGER PRIMARY KEY,
                team_id INTEGER,
                name TEXT,
                initials TEXT,
                gender TEXT,
                position TEXT,
                accuracy REAL,
                balance REAL,
                charisma REAL,
                competitiveness REAL,
                cowardice REAL,
                dramatic_flair REAL,
                goutiness REAL,
                greed REAL,
                integrity REAL,
                intelligence REAL,
                metabolism REAL,
                neoliberalism REAL,
                power REAL,
                savagery REAL,
                solidity REAL,
                speed REAL,
                stamina REAL,
                visual_calculus REAL,
                FOREIGN KEY (team_id) REFERENCES teams (id)
            )
        ''')

    def insert_team(self, team):
        self.cursor.execute('INSERT INTO teams (name) VALUES (?)', (team.name,))
        team_id = self.cursor.lastrowid

        for player in team.players:
            self.cursor.execute('INSERT INTO players (team_id, name, initials, gender, position, accuracy, balance, charisma, competitiveness, cowardice, dramatic_flair, goutiness, greed, integrity, intelligence, metabolism, neoliberalism, power, savagery, solidity, speed, stamina, visual_calculus) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (team_id, player.name, player.initials, player.gender, player.position, player.accuracy, player.balance, player.charisma, player.competitiveness, player.cowardice, player.dramatic_flair, player.goutiness, player.greed, player.integrity, player.intelligence, player.metabolism, player.neoliberalism, player.power, player.savagery, player.solidity, player.speed, player.stamina, player.visual_calculus))

        self.conn.commit()

    def get_table(self, table_name):
        self.cursor.execute(f'SELECT * FROM {table_name}')
        rows = self.cursor.fetchall()

        for row in rows:
            print(row)
    
db = Database('battle_golf.db')
db.create_tables()

positions = ['driver', 'driver', 'blocker', 'blocker', 'marksman', 'goalie', 'caddy']

teams = []

for team_id in range(1, 9):  # This will loop from 1 to 8
    players = []
    for position in positions:
        players.append(Player(team_id=team_id, position=position))
    
    team_name = team_names.get(team_id, f"Team {team_id}")
    team = Team(name=team_name, players=players)
    teams.append(team)

for team in teams:
    db.insert_team(team)

db.cursor.execute("SELECT * FROM players")
rows = db.cursor.fetchall()
for row in rows:
    print(row)