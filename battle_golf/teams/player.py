import sqlite3
import random
import string

class Player:
    def __init__(self, position, name=None, gender=None, accuracy=None, balance=None, charisma=None,
                 competitiveness=None, cowardice=None, dramatic_flair=None, goutiness=None,
                 greed=None, integrity=None, metabolism = None, neoliberalism=None, power=None, savagery=None,
                 solidity=None, speed=None, stamina=None, visual_calculus=None):
        self.position = position
        self.name = name or self.generate_name()
        self.gender = gender or self.invent_gender()
        self.accuracy = round(accuracy or random.uniform(1.0, 10.0), 2)
        self.balance = round(balance or random.uniform(1.0, 10.0), 2)
        self.charisma = round(charisma or random.uniform(1.0, 10.0), 2)
        self.competitiveness = round(competitiveness or random.uniform(1.0, 10.0), 2)
        self.cowardice = round(cowardice or random.uniform(1.0, 10.0), 2)
        self.dramatic_flair = round(dramatic_flair or random.uniform(1.0, 10.0), 2)
        self.goutiness = round(goutiness or random.uniform(1.0, 10.0), 2)
        self.greed = round(greed or random.uniform(1.0, 10.0), 2)
        self.integrity = round(integrity or random.uniform(1.0, 10.0), 2)
        self.metabolism = round(metabolism or random.uniform(1.0, 10.0), 2)
        self.neoliberalism = round(neoliberalism or random.uniform(1.0, 10.0), 2)
        self.power = round(power or random.uniform(1.0, 10.0), 2)
        self.savagery = round(savagery or random.uniform(1.0, 10.0), 2)
        self.solidity = round(solidity or random.uniform(1.0, 10.0), 2)
        self.speed = round(speed or random.uniform(1.0, 10.0), 2)
        self.stamina = round(stamina or random.uniform(1.0, 10.0), 2)
        self.visual_calculus = round(visual_calculus or random.uniform(1.0, 10.0), 2)
        self.weighted_stats(position, self.accuracy, self.balance, self.charisma, self.competitiveness, self.cowardice, self.dramatic_flair, self.goutiness, self.greed, self.integrity, self.metabolism, self.neoliberalism, self.power, self.savagery, self.solidity, self.speed, self.stamina, self.visual_calculus)

    def generate_name(self):
        with open('names/first_names.txt') as f:
            first_names = [line.strip() for line in f]
        with open('names/last_names.txt') as f:
            last_names = [line.strip() for line in f]
        return random.choice(first_names) + ' ' + random.choice(last_names)
    
    def invent_gender(self):
        letters = string.ascii_lowercase
        gender = ''.join(random.choices(letters, k=random.randint(1, 3))).upper()
        # Read the blacklisted words from the file
        with open('names/blacklisted.txt', 'r') as f:
            blacklisted_words = f.read().splitlines()
        # Check if the generated gender is in the blacklisted words
        if gender in blacklisted_words:
            return self.invent_gender()

        return gender

    def weighted_stats(self, position, accuracy, balance, charisma, competitiveness, cowardice, dramatic_flair, goutiness, greed, integrity, metabolism, neoliberalism, power, savagery, solidity, speed, stamina, visual_calculus):
        if position == 'driver':
            accuracy *= random.uniform(1.0, 1.3)
            power *= random.uniform(1.0, 1.7)
            stamina *= random.uniform(1.0, 1.2)
            speed *= random.uniform(0.5, 1.0)
        elif position == 'blocker':
            accuracy *= random.uniform(0.7, 1.0)
            balance *= random.uniform(1.0, 1.3)
            competitiveness *= random.uniform(1.5, 2.3)
            greed *= random.uniform(1.1, 1.2)
            power *= random.uniform(0.2, 0.6)
            solidity *= random.uniform(1.1, 1.4)
            speed *= random.uniform(1.1, 1.4)
        elif position == 'marksman':
            accuracy *= random.uniform(1.2, 1.6)
            competitiveness *= random.uniform(1.5, 2.5)
            cowardice *= random.uniform(0.5, 0.8)
            dramatic_flair *= random.uniform(1.1, 3.0)
            power *= random.uniform(1.5, 1.6)
            savagery *= random.uniform(1.1, 1.5)
            speed *= random.uniform(0.5, 1.0)
            stamina *= random.uniform(0.8, 1.2)
        elif position == 'goalie':
            balance *= random.uniform(1.1, 1.7)
            cowardice *= random.uniform(0.5, 0.8)
            dramatic_flair *= random.uniform(1.1, 1.6)
            solidity *= random.uniform(1.1, 1.6)
            stamina *= random.uniform(1.2, 1.6)
            speed *= random.uniform(1.5, 2.0)
        else:
            accuracy *= random.uniform(0.8, 1.2)
            power *= random.uniform(0.8, 1.2)
            stamina *= random.uniform(0.8, 1.2)
            speed *= random.uniform(0.8, 1.2)
        return round(accuracy, 2), round(power, 2), round(stamina, 2), round(speed, 2)

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
                gender TEXT,
                position TEXT,
                power REAL,
                accuracy REAL,
                balance REAL,
                charisma REAL,
                competitiveness REAL,
                cowardice REAL,
                dramatic_flair REAL,
                goutiness REAL,
                greed REAL,
                integrity REAL,
                metabolism REAL,
                neoliberalism REAL,
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
            self.cursor.execute('INSERT INTO players (team_id, name, gender, position, power, accuracy, balance, charisma, competitiveness, cowardice, dramatic_flair, goutiness, greed, integrity, metabolism, neoliberalism, savagery, solidity, speed, stamina, visual_calculus) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (team_id, player.name, player.gender, player.position, player.power, player.accuracy, player.balance, player.charisma, player.competitiveness, player.cowardice, player.dramatic_flair, player.goutiness, player.greed, player.integrity, player.metabolism, player.neoliberalism, player.savagery, player.solidity, player.speed, player.stamina, player.visual_calculus))

        self.conn.commit()

    def get_table(self, table_name):
        self.cursor.execute(f'SELECT * FROM {table_name}')
        rows = self.cursor.fetchall()

        for row in rows:
            print(row)
    
db = Database('battle_golf.db')
db.create_tables()

teams = [
    Team(name='Team A', players=[Player(position='driver'), Player(position='driver'), Player(position='blocker'), Player(position='blocker'), Player(position='marksman'), Player(position='goalie')]),
    Team(name='Team B', players=[Player(position='driver'), Player(position='driver'), Player(position='blocker'), Player(position='blocker'), Player(position='marksman'), Player(position='goalie')]),
    Team(name='Team C', players=[Player(position='driver'), Player(position='driver'), Player(position='blocker'), Player(position='blocker'), Player(position='marksman'), Player(position='goalie')]),
    Team(name='Team D', players=[Player(position='driver'), Player(position='driver'), Player(position='blocker'), Player(position='blocker'), Player(position='marksman'), Player(position='goalie')]),
    Team(name='Team E', players=[Player(position='driver'), Player(position='driver'), Player(position='blocker'), Player(position='blocker'), Player(position='marksman'), Player(position='goalie')]),
    Team(name='Team F', players=[Player(position='driver'), Player(position='driver'), Player(position='blocker'), Player(position='blocker'), Player(position='marksman'), Player(position='goalie')]),
    Team(name='Team G', players=[Player(position='driver'), Player(position='driver'), Player(position='blocker'), Player(position='blocker'), Player(position='marksman'), Player(position='goalie')]),
    Team(name='Team H', players=[Player(position='driver'), Player(position='driver'), Player(position='blocker'), Player(position='blocker'), Player(position='marksman'), Player(position='goalie')])
]

for team in teams:
    db.insert_team(team)

db.get_table('players')