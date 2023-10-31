import random
import string
import sqlite3

class Player:
    def __init__(self, team_id, position, name=None, initials=None, gender=None, coordinates=None, accuracy=None, balance=None, charisma=None,
                 competitiveness=None, cowardice=None, dramatic_flair=None, goutiness=None,
                 greed=None, integrity=None, intelligence=None, metabolism = None, neoliberalism=None, power=None, savagery=None,
                 solidity=None, speed=None, stamina=None, visual_calculus=None):
        self.team_id = team_id
        self.position = position
        self.name = name or self.generate_name()
        self.initials = initials or ''.join([word[0] for word in self.name.split(' ')])
        self.gender = gender or self.invent_gender()
        self.coordinates = coordinates or (0,0)
        self.accuracy = round(accuracy or random.uniform(1.0, 10.0), 2)
        self.balance = round(balance or random.uniform(1.0, 10.0), 2)
        self.charisma = round(charisma or random.uniform(1.0, 10.0), 2)
        self.competitiveness = round(competitiveness or random.uniform(1.0, 10.0), 2)
        self.cowardice = round(cowardice or random.uniform(1.0, 10.0), 2)
        self.dramatic_flair = round(dramatic_flair or random.uniform(1.0, 10.0), 2)
        self.goutiness = round(goutiness or random.uniform(1.0, 10.0), 2)
        self.greed = round(greed or random.uniform(1.0, 10.0), 2)
        self.integrity = round(integrity or random.uniform(1.0, 10.0), 2)
        self.intelligence = round(intelligence or random.uniform(1.0, 10.0), 2)
        self.metabolism = round(metabolism or random.uniform(1.0, 10.0), 2)
        self.neoliberalism = round(neoliberalism or random.uniform(1.0, 10.0), 2)
        self.power = round(power or random.uniform(1.0, 10.0), 2)
        self.savagery = round(savagery or random.uniform(1.0, 10.0), 2)
        self.solidity = round(solidity or random.uniform(1.0, 10.0), 2)
        self.speed = round(speed or random.uniform(1.0, 10.0), 2)
        self.stamina = round(stamina or random.uniform(1.0, 10.0), 2)
        self.visual_calculus = round(visual_calculus or random.uniform(1.0, 10.0), 2)
        self.weighted_stats(position, self.accuracy, self.balance, self.charisma, self.competitiveness, self.cowardice, self.dramatic_flair, self.goutiness, self.greed, self.integrity, self.intelligence, self.metabolism, self.neoliberalism, self.power, self.savagery, self.solidity, self.speed, self.stamina, self.visual_calculus)

    def generate_name(self):
        with open('../teams/names/first_names.txt') as f:
            first_names = [line.strip() for line in f]
        with open('../teams/names/last_names.txt') as f:
            last_names = [line.strip() for line in f]
        return random.choice(first_names) + ' ' + random.choice(last_names)
    
    def invent_gender(self):
        letters = string.ascii_lowercase
        gender = ''.join(random.choices(letters, k=random.randint(1, 3))).upper()
        # Read the blacklisted words from the file
        with open('../teams/names/blacklisted.txt', 'r') as f:
            blacklisted_words = f.read().splitlines()
        # Check if the generated gender is in the blacklisted words
        if gender in blacklisted_words:
            return self.invent_gender()

        return gender

    def weighted_stats(self, position, accuracy, balance, charisma, competitiveness, cowardice, dramatic_flair, goutiness, greed, integrity, intelligence, metabolism, neoliberalism, power, savagery, solidity, speed, stamina, visual_calculus):
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
            visual_calculus *= random.uniform(1.1, 1.5)
        elif position == 'goalie':
            balance *= random.uniform(1.1, 1.7)
            cowardice *= random.uniform(0.5, 0.8)
            dramatic_flair *= random.uniform(1.1, 1.6)
            solidity *= random.uniform(1.1, 1.6)
            stamina *= random.uniform(1.2, 1.6)
            speed *= random.uniform(1.5, 2.0)
        elif position == 'caddy':
            charisma *= random.uniform(1.1, 1.6)
            competitiveness *= random.uniform(1.1, 1.6)
            cowardice *= random.uniform(1.1, 1.6)
            dramatic_flair *= random.uniform(1.5, 3.0)
            goutiness *= random.uniform(0.9, 1.3)
            greed*= random.uniform(1.2, 1.4)
            integrity *= random.uniform(1.5, 2.0)
            intelligence *= random.uniform(0.4, 0.99)
            savagery *= random.uniform(0.5, 0.8)
        else:
            accuracy *= random.uniform(0.8, 1.2)
            power *= random.uniform(0.8, 1.2)
            stamina *= random.uniform(0.8, 1.2)
            speed *= random.uniform(0.8, 1.2)
        return round(accuracy, 2), round(power, 2), round(stamina, 2), round(speed, 2)
        
    def get_players_from_db():
        conn = sqlite3.connect('../teams/battle_golf.db')
        cursor = conn.cursor()

        cursor.execute("SELECT team_id, name, initials, gender, position, accuracy, balance, charisma, competitiveness, cowardice, dramatic_flair, goutiness, greed, integrity, intelligence, metabolism, neoliberalism, power, savagery, solidity, speed, stamina, visual_calculus FROM players")
        data = cursor.fetchall()

        conn.close()

        players = []
        for row in data:
            player = Player(
                team_id=row[0],
                name=row[1],
                initials=row[2],
                gender=row[3],
                position=row[4],
                power=row[5],
                accuracy=row[6],
                # ... and so on for the other attributes
            )
            players.append(player)

        return players

    
    def move(self, target_coordinates):
        direction = [target_coordinates[0] - self.coordinates[0] , target_coordinates[1] - self.coordinates[1]]
        distance = (direction[0]**2 + direction[1]**2)**0.5
        
        if distance > 1:
            direction = [direction[0] / distance, direction[1] / distance]

        adjusted_speed = self.speed * (self.competitiveness / self.cowardice) * random.uniform(0.7, 1.3)

        self.coordinates[0] += direction[0] * adjusted_speed
        self.coordinates[1] += direction[1] * adjusted_speed

        if (self.coordinates[0] - target_coordinates[0])**2 + (self.coordinates[1] - target_coordinates[1])**2 < adjusted_speed**2:
            self.coordinates = target_coordinates
