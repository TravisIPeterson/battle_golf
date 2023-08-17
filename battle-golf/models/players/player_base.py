import random
import numpy as np
from .actions.offensive_actions import OffensiveActions
from .actions.defensive_actions import DefensiveActions
from .actions.miscellaneous_actions import MiscellaneousActions

class Player:
    MAX_SPEED = 20  # Maximum speed a player can achieve

    def __init__(self, role, team_name, green_number=1, stats=None):
        self.role = role
        self.stats = stats if stats else {
            key: random.randint(1, 20) for key in [
                'Power', 'Accuracy', 'Speed', 'Visual Calculus', 'Balance', 
                'Solidity', 'Savagery', 'Competitiveness', 'Cowardice', 'Neoliberalism',
                'Integrity'
            ]
        }
        self.green_number = green_number
        self.team_name = team_name

    def calculate_speed(self):
        """Calculate player's speed based on various factors."""
        speed = self.stats['Speed'] * random.uniform(0.9, 1.1)
        balance_factor = self.stats['Balance'] / 20.0  # normalize to [0.05, 1]
        speed *= balance_factor
        competitiveness_boost = (self.stats['Competitiveness'] - 10) / 100.0  # results in [-0.1, 0.1]
        speed += speed * competitiveness_boost
        return min(speed, self.MAX_SPEED)

    def display_stats(self):
        print(f"Role: {self.role}")
        for stat, value in self.stats.items():
            print(f"{stat}: {value}")

    def should_go_for_ball(self, ball_green, num_pursuers):
        print(f"{self.role} is deciding whether to pursue the ball.")
        # Assuming there's a max chance for the first pursuer, which decreases by 20% for each subsequent pursuer
        chance = 1.0 - num_pursuers * 0.2
        decision = random.random() <= chance

        # Check if the player is on the same green as the ball
        if self.green_number != ball_green:
            decision = False

        # Prioritize actions based on player roles
        if self.role in ["blocker", "driver", "marksman", "goalie"]:
            return decision

        if decision:
            print(random.choice([f"{self.role.capitalize()} decided to go for the ball!",
                                f"{self.role.capitalize()} is making a move towards the ball!",
                                f"Watch out! The {self.role} is on the move!"]))
        else:
            print(random.choice([f"{self.role.capitalize()} chose to stay put.",
                                f"{self.role.capitalize()} is playing it safe.",
                                f"Seems like the {self.role} is biding their time."]))
        return decision

    def select_green(self):
        num_greens = 8
        greens = list(range(1, num_greens + 1))

        difference = self.stats["Competitiveness"] - self.stats["Cowardice"]
        factor = abs(difference) / 10.0  # Scaling factor to adjust probabilities

        rival_green = (self.green_number + num_greens // 2 - 1) % num_greens + 1

        # Initialize with equal probabilities
        probabilities = [1 / num_greens] * num_greens

        if difference > 0:  # Competitiveness dominates
            for i in range(num_greens):
                distance_from_rival = abs(rival_green - i - 1)
                # Using exponential decay for bias
                probabilities[i] += factor * np.exp(-distance_from_rival)
        elif difference < 0:  # Cowardice dominates
            # [omitted the part that determines cowardice dominance, as it's tied to position]

            # Normalize the probabilities to sum up to 1
            total = sum(probabilities)
            probabilities = [p / total for p in probabilities]

        selected_green = np.random.choice(greens, p=probabilities)
        print(random.choice([f"{self.role.capitalize()} is aiming for Green {selected_green}.",
                             f"Looks like Green {selected_green} is the target!",
                             f"{self.role.capitalize()} has Green {selected_green} in sight."]))
        return selected_green