import random
import string
import sqlite3
import math
from game_logic.game_state import Coordinates

class Player:
    def __init__(self, team_id, position, name=None, initials=None, gender=None, accuracy=None, balance=None, charisma=None,
                 competitiveness=None, cowardice=None, dramatic_flair=None, goutiness=None,
                 greed=None, integrity=None, intelligence=None, metabolism = None, neoliberalism=None, power=None, savagery=None,
                 solidity=None, speed=None, stamina=None, tenacity=None, twitchiness=None, visual_calculus=None):
        self.team_id = team_id
        self.position = position
        self.name = name or self.generate_name()
        self.initials = initials or ''.join([word[0] for word in self.name.split(' ')])
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
        self.intelligence = round(intelligence or random.uniform(1.0, 10.0), 2)
        self.metabolism = round(metabolism or random.uniform(1.0, 10.0), 2)
        self.neoliberalism = round(neoliberalism or random.uniform(1.0, 10.0), 2)
        self.power = round(power or random.uniform(1.0, 10.0), 2)
        self.savagery = round(savagery or random.uniform(1.0, 10.0), 2)
        self.solidity = round(solidity or random.uniform(1.0, 10.0), 2)
        self.speed = round(speed or random.uniform(1.0, 10.0), 2)
        self.stamina = round(stamina or random.uniform(1.0, 10.0), 2)
        self.tenacity = round(tenacity or random.uniform(1.0, 10.0), 2)
        self.twitchiness = round(random.uniform(1.0, 10.0), 2)
        self.visual_calculus = round(visual_calculus or random.uniform(1.0, 10.0), 2)
        self.weighted_stats(position, self.accuracy, self.balance, self.charisma, self.competitiveness, self.cowardice, self.dramatic_flair, self.goutiness, self.greed, self.integrity, self.intelligence, self.metabolism, self.neoliberalism, self.power, self.savagery, self.solidity, self.speed, self.stamina, self.tenacity, self.twitchiness, self.visual_calculus)
        self.coordinates = Coordinates()
        self.targeted_ball = None
        self.action_in_progress = None
        self.action_completed = False
        self.targeted_opponent = None
        self.target_coordinates = self.coordinates
        self.personal_clock = 0

    @property
    def x(self):
        return self.coordinates.x

    @property
    def y(self):
        return self.coordinates.y

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

    def weighted_stats(self, position, accuracy, balance, charisma, competitiveness, cowardice, dramatic_flair, goutiness, greed, integrity, intelligence, metabolism, neoliberalism, power, savagery, solidity, speed, stamina, tenacity, twitchiness, visual_calculus):
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
            speed *= random.uniform(1.5, 2.0)
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
            speed *= random.uniform(1.0, 1.5)
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
            twitchiness *= random.uniform(1.1, 2.0)
        else:
            accuracy *= random.uniform(0.8, 1.2)
            power *= random.uniform(0.8, 1.2)
            stamina *= random.uniform(0.8, 1.2)
            speed *= random.uniform(0.8, 1.2)
        return round(accuracy, 2), round(power, 2), round(stamina, 2), round(speed, 2)
        
    def get_players_from_db():
        conn = sqlite3.connect('../teams/battle_golf.db')
        cursor = conn.cursor()

        cursor.execute("SELECT team_id, name, initials, gender, position, accuracy, balance, charisma, competitiveness, cowardice, dramatic_flair, goutiness, greed, integrity, intelligence, metabolism, neoliberalism, power, savagery, solidity, speed, stamina, tenacity, twitchiness, visual_calculus FROM players")
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
                accuracy=row[5],
                balance=row[6],
                charisma=row[7],
                competitiveness=row[8],
                cowardice=row[9],
                dramatic_flair=row[10],
                goutiness=row[11],
                greed=row[12],
                integrity=row[13],
                intelligence=row[14],
                metabolism=row[15],
                neoliberalism=row[16],
                power=row[17],
                savagery=row[18],
                solidity=row[19],
                speed=row[20],
                stamina=row[21],
                tenacity=row[22],
                twitchiness=row[23],
                visual_calculus=row[24]
            )
            player.coordinates = Coordinates()
            players.append(player)

        return players

    def move(self, target_coordinates, greens, wind):
        # Extract x and y from the target_coordinates if it's not a tuple (for safety)
        target_x, target_y = target_coordinates if isinstance(target_coordinates, tuple) else (target_coordinates.x, target_coordinates.y)

        # Calculate the direction vector components
        direction_x = target_x - self.coordinates.x
        direction_y = target_y - self.coordinates.y
        distance_to_target = (direction_x**2 + direction_y**2)**0.5

        # Normalize the direction vector to length 1 if the distance is greater than 1
        if distance_to_target > 1:
            direction_x /= distance_to_target
            direction_y /= distance_to_target

        # Calculate the new potential position
        adjusted_speed = ((self.speed + self.metabolism + self.stamina) / self.goutiness) * 0.1
        if adjusted_speed < 0.5:
            adjusted_speed = 0.5
        if adjusted_speed > 1.75:
            adjusted_speed = 1.75
        new_x = self.coordinates.x + direction_x * adjusted_speed
        new_y = self.coordinates.y + direction_y * adjusted_speed

        # Check if the new position is on the green of another team
        if not self.position == 'blocker' or not self.position == 'goalie':
            for green in greens:
                if green.team != self.team_id and green.contains(new_x, new_y):
                    # The new position is on another team's green, do not update the position
                    self.action_in_progress = None
                    self.targeted_ball = None
                    # Have the player turn around and move away from the green
                    self.coordinates.x -= direction_x * adjusted_speed
                    self.coordinates.y -= direction_y * adjusted_speed
                    return

        # Check if the player has reached the target coordinates and update accordingly
        if (new_x - target_x)**2 + (new_y - target_y)**2 < adjusted_speed**2:
            self.coordinates.x = target_x
            self.coordinates.y = target_y
        else:
            self.coordinates.x = new_x
            self.coordinates.y = new_y
        
    def get_prediction_frames(self, ball):
        base_frames = 30
        max_height = 100

        if ball.is_ascending():
            height_factor = ball.z / max_height
            frames_ahead = base_frames * height_factor
        else:
            height_factor = (max_height - ball.z) / max_height
            frames_ahead = base_frames * (1 - height_factor)

        intelligence_factor = self.intelligence / random.uniform(5, 10)
        visual_calculus_factor = self.visual_calculus / random.uniform(5, 10)
        frames_adjustment = (intelligence_factor + visual_calculus_factor)

        final_prediction_frames = max(1, frames_ahead * frames_adjustment)

        return int(final_prediction_frames)

    def aim(self, greens, wind):
        # Calculate rivalry scores
        rivalry_scores = [(self.team_id - green.team) % 8 for green in greens]
        # Sort greens by rivalry score (ascending)
        greens = [green for _, green in sorted(zip(rivalry_scores, greens))]
        # Select target green based on competitiveness, dramatic flair, and cowardice
        feeling_feisty = self.competitiveness * self.dramatic_flair / (self.cowardice + self.savagery)
        if feeling_feisty > random.uniform(7, 10):
            # Target green with rivalry score of 4
            target_green = greens[rivalry_scores.index(4)] if 4 in rivalry_scores else random.choice(greens)
        elif feeling_feisty > random.uniform(5, 7):
            # Target green with rivalry score of 3 or 5
            target_green = greens[rivalry_scores.index(random.choice([3, 5]))] if any(i in rivalry_scores for i in [3, 5]) else random.choice(greens)
        elif feeling_feisty > random.uniform(3, 5):
            # Target green with rivalry score of 2 or 6
            target_green = greens[rivalry_scores.index(random.choice([2, 6]))] if any(i in rivalry_scores for i in [2, 6]) else random.choice(greens)
        else:
            # Target green with rivalry score of 1 or 7
            target_green = greens[rivalry_scores.index(random.choice([1, 7]))] if any(i in rivalry_scores for i in [1, 7]) else random.choice(greens)
        if target_green == self.team_id:
            # Target green is own team's green, choose a random green instead but not the same one as before
            target_green = random.choice([green for green in greens if green != self.team_id])
        # Calculate direction towards center of target green, factoring in visual calculus and intelligence
        dx = target_green.hole_x - self.x
        dy = target_green.hole_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        direction_x = dx / distance * (1 + self.visual_calculus / 10)  # Higher visual_calculus leads to more accurate direction
        direction_y = dy / distance * (1 + self.visual_calculus / 10)  # Higher visual_calculus leads to more accurate direction
        # Adjust for wind direction and speed, factoring in intelligence
        wind_direction_vector, wind_speed = wind.get_direction_vector()
        direction_x -= wind_direction_vector[0] * wind_speed * (1 - self.intelligence / 10)  # Higher intelligence leads to better wind adjustment
        direction_y -= wind_direction_vector[1] * wind_speed * (1 - self.intelligence / 10)  # Higher intelligence leads to better wind adjustment
        return direction_x, direction_y
    
    def aim_at_opponent(self, opponent):
        # Calculate direction towards opponent, factoring in visual calculus and intelligence
        dx = opponent.x - self.x
        dy = opponent.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            distance = 1
            
        direction_x = dx / distance * (1 + self.visual_calculus * self.accuracy / 10)
        direction_y = dy / distance * (1 + self.visual_calculus * self.accuracy / 10)
        return direction_x, direction_y
    
    def is_hit(self, ball):
        # Calculate distance between player and ball
        dx = ball.x - self.x
        dy = ball.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Calculate the chance of hitting the ball
        if ball.last_hit_by:
            if distance < 1 and random.random() < 0.01 and ball.last_hit_by.team_id != self.team_id:
                if (ball.velocity[0] * ball.velocity[1]) > (self.solidity * self.metabolism  + self.balance + self.tenacity) / self.goutiness:
                    if self.position == 'blocker' and random.random() < 0.2:
                        return False
                    if self.position == 'goalie' and random.random() < 0.2:
                        return False
                    return True
                return True
            
    def calculate_hit_consequences(self, ball):
        variable_names = {
            'accuracy': self.accuracy,
            'balance': self.balance,
            'charisma': self.charisma,
            'competitiveness': self.competitiveness,
            'cowardice': self.cowardice,
            'dramatic_flair': self.dramatic_flair,
            'goutiness': self.goutiness,
            'greed': self.greed,
            'integrity': self.integrity,
            'intelligence': self.intelligence,
            'metabolism': self.metabolism,
            'neoliberalism': self.neoliberalism,
            'power': self.power,
            'savagery': self.savagery,
            'solidity': self.solidity,
            'speed': self.speed,
            'stamina': self.stamina,
            'tenacity': self.tenacity,
            'twitchiness': self.twitchiness,
            'visual_calculus': self.visual_calculus
        }
    # Divide a random player stat by velocity of the ball
        variable_name = random.choice(list(variable_names.keys()))
        affected_stat = variable_names[variable_name]

        # Update the player's attribute
        setattr(self, variable_name, affected_stat / random.uniform(0.9, 2))
        if affected_stat > 10:
            setattr(self, variable_name, affected_stat % 10)
        print(f"{self.name} got hit! Their {variable_name} is now {affected_stat}.")