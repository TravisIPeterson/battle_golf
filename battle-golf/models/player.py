import random
import numpy as np
from .ball import Ball

class Player:
    def __init__(self, role, stats=None):
        self.role = role
        self.stats = stats if stats else {
            key: random.randint(1, 20) for key in [
                'Power', 'Accuracy', 'Speed', 'Visual Calculus', 'Balance', 
                'Solidity', 'Savagery', 'Competitiveness', 'Cowardice', 'Neoliberalism'
            ]
        }
        self.position = (0, 0)
        self.green_number = random.randint(1, 8)

    def display_stats(self):
        print(f"Role: {self.role}")
        for stat, value in self.stats.items():
            print(f"{stat}: {value}")

    def select_green(self):
        num_greens = 8
        greens = list(range(1, num_greens + 1))

        difference = self.stats["Competitiveness"] - self.stats["Cowardice"]
        factor = abs(difference) / 10.0  # Scaling factor to adjust probabilities

        rival_green = (self.green_number + num_greens // 2 - 1) % num_greens + 1
        left_neighbor = (self.green_number - 1) % num_greens + 1
        right_neighbor = (self.green_number + 1) % num_greens + 1

        # Initialize with equal probabilities
        probabilities = [1 / num_greens] * num_greens

        if difference > 0:  # Competitiveness dominates
            for i in range(num_greens):
                distance_from_rival = abs(rival_green - i - 1)
                # Using exponential decay for bias
                probabilities[i] += factor * np.exp(-distance_from_rival)

        elif difference < 0:  # Cowardice dominates
            for i in range(num_greens):
                distance_from_left = abs(left_neighbor - i - 1)
                distance_from_right = abs(right_neighbor - i - 1)
                min_distance = min(distance_from_left, distance_from_right)
                # Using exponential decay for bias
                probabilities[i] += factor * np.exp(-min_distance)

        # Normalize the probabilities to sum up to 1
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]

        chosen_green = np.random.choice(greens, p=probabilities)
        return chosen_green

    def drive(self, target_green, rival_green_number):
        # Uses the 'Power', 'Accuracy', and 'Competitiveness' stats
        force = self.stats['Power'] * random.uniform(0.9, 1.1)
        accuracy = self.stats['Accuracy'] * random.uniform(0.9, 1.1)
        competitiveness = self.stats['Competitiveness'] * random.uniform(0.9, 1.1)
        
        # Calculate the rivalry intensity based on proximity to the rival's green
        green_difference = abs(target_green.number - rival_green_number)
        if green_difference == 0:
            rivalry_intensity = 1  # Maximum intensity when targeting the rival's green directly
        else:
            rivalry_intensity = 1.0 / green_difference
        
        # Modify power and accuracy based on competitiveness and rivalry intensity
        competitive_boost = 1 + (competitiveness / 20.0 * rivalry_intensity)
        force *= competitive_boost
        accuracy *= competitive_boost
        
        # Calculate distance the ball is hit based on Power
        max_distance = 100  # Assuming a maximum possible distance a ball can be hit
        distance_hit = force / 20.0 * max_distance  # Normalize power to a fraction of max_distance

        # Determine deviation from target based on Accuracy
        max_deviation = 10  # Maximum deviation in any direction from the target
        deviation_x = (random.uniform(-1, 1) * (1 - accuracy / 20.0) * max_deviation)
        deviation_y = (random.uniform(-1, 1) * (1 - accuracy / 20.0) * max_deviation)
        
        # Determine ball's landing coordinates
        target_x, target_y = target_green.position
        landing_x = target_x + deviation_x
        landing_y = target_y + deviation_y

        # If the ball lands on the green, calculate distance from the hole
        if target_green.is_within_boundary((landing_x, landing_y)):
            distance_from_hole = target_green.distance_from_center((landing_x, landing_y))
        else:
            distance_from_hole = None

        # Update the ball's position to landing coordinates
        ball = Ball()  # This would be a reference to the actual ball object in your game
        ball.position = (landing_x, landing_y)
        
        return landing_x, landing_y, distance_from_hole

    def block(self, ball):
        # Get the relative speed of the player (how fast they can move to block the ball)
        speed = self.stats['Speed'] * random.uniform(0.9, 1.1)

        # Visual Calculus factor
        # A player with a higher visual calculus will "see" the trajectory better and react faster.
        visual_calculus_factor = self.stats['Visual Calculus'] / 100.0  # normalize to [0, 1]
        reaction_time = 1 - visual_calculus_factor  # assuming that a higher visual calculus results in a shorter reaction time

        # Calculate the effective time the player has to block the ball
        # Assuming the ball's distance from the player and its speed towards the player give a time_to_impact value
        time_to_impact = distance_from_ball_to_player / ball_speed_towards_player
        effective_time = time_to_impact - reaction_time

        # Player's success at blocking is affected by their solidity and if they flinch (cowardice)
        solidity_factor = self.stats['Solidity'] / 100.0
        cowardice_factor = random.uniform(0, 1) * (100 - self.stats['Cowardice']) / 100.0  # higher cowardice reduces this factor

        block_success_chance = speed * solidity_factor * cowardice_factor * effective_time

        # If the block_success_chance is greater than some threshold, then the block is successful.
        # Adjust the threshold based on gameplay requirements.
        BLOCK_THRESHOLD = 0.7
        if block_success_chance > BLOCK_THRESHOLD:
            ball.position = self.position  # update the ball's position to be with the blocker
            return True  # block is successful

        return False  # block failed


    def aimed_shot(self, greens, players):
        # Use competitiveness to target a green, similar to the drive method
        num_greens = len(greens)
        greens_probabilities = [1 / float(num_greens)] * num_greens

        rival_green = (self.green_number + num_greens // 2 - 1) % num_greens + 1
        competitiveness_factor = (self.stats['Competitiveness'] - 10) / 10.0
        greens_probabilities[rival_green - 1] += competitiveness_factor * 0.1

        chosen_green = np.random.choice(greens, p=greens_probabilities)

        # Determine if the player aims for the hole or another player based on savagery
        aim_for_player = random.random() < (self.stats['Savagery'] / 20.0)

        if aim_for_player:
            # Choose a player to target; in a more refined version, this could consider player positions, roles, etc.
            targeted_player = random.choice(players)

            # Targeted position is the position of the chosen player
            target_x, target_y = targeted_player.position
        else:
            # Targeted position is the hole of the chosen green
            target_x, target_y = chosen_green.position

        # Calculate deviation from target based on accuracy
        max_deviation = 10  # Assuming a set max deviation
        deviation_x = (random.uniform(-1, 1) * (1 - self.stats['Accuracy'] / 20.0) * max_deviation)
        deviation_y = (random.uniform(-1, 1) * (1 - self.stats['Accuracy'] / 20.0) * max_deviation)

        shot_x = target_x + deviation_x
        shot_y = target_y + deviation_y

        return shot_x, shot_y, aim_for_player

    def save(self, ball):
        # Speed: how quickly the player can move to intercept the ball
        speed = self.stats['Speed'] * random.uniform(0.9, 1.1)

        # Visual Calculus factor
        visual_calculus_factor = self.stats['Visual Calculus'] / 100.0  # normalize to [0, 1]
        reaction_time = 1 - visual_calculus_factor  # assuming that a higher visual calculus results in a shorter reaction time

        # Calculate the effective time the player has to save the ball
        time_to_impact = distance_from_ball_to_goal / ball_speed_towards_goal
        effective_time = time_to_impact - reaction_time

        # Player's success at saving is also affected by their solidity
        solidity_factor = self.stats['Solidity'] / 100.0
        
        # Cowardice factor: do they flinch from the incoming ball?
        cowardice_factor = random.uniform(0, 1) * (100 - self.stats['Cowardice']) / 100.0
        
        # Balance on the sloped green near the hole
        balance_factor = self.stats['Balance'] / 100.0

        save_success_chance = speed * solidity_factor * cowardice_factor * effective_time * balance_factor

        # If the save_success_chance is greater than some threshold, then the save is successful.
        # Adjust the threshold based on gameplay requirements.
        SAVE_THRESHOLD = 0.8
        if save_success_chance > SAVE_THRESHOLD:
            ball.position = self.position  # update the ball's position to be with the goalkeeper
            return True  # save is successful

        # Consider potential of player falling into the hole if balance is bad and they missed the save
        FALL_THRESHOLD = 0.3
        if balance_factor < FALL_THRESHOLD and save_success_chance < SAVE_THRESHOLD:
            # Handle the logic for the player falling into the hole
            self.fall_into_hole()

        return False  # save failed


    def run_toward_ball(self, ball_position):
        # Calculate base movement speed
        speed = self.stats['Speed'] * random.uniform(0.9, 1.1)

        # Factor in balance on the sloped green
        balance_factor = self.stats['Balance'] / 20.0  # normalize to [0.05, 1]
        speed *= balance_factor

        # Add competitiveness boost
        competitiveness_boost = (self.stats['Competitiveness'] - 10) / 100.0  # results in [-0.1, 0.1]
        speed += speed * competitiveness_boost

        # Cap the max speed
        MAX_SPEED = 20  # Arbitrarily chosen, you can modify based on your needs
        speed = min(speed, MAX_SPEED)

        # Calculate new position based on speed and direction towards the ball
        direction_to_ball_x = ball_position[0] - self.position[0]
        direction_to_ball_y = ball_position[1] - self.position[1]

        # Normalize the direction
        magnitude = (direction_to_ball_x**2 + direction_to_ball_y**2)**0.5

        # Check if player is already close to the ball, and if so, possibly reduce the speed
        CLOSE_DISTANCE = 5  # Arbitrarily chosen
        if magnitude < CLOSE_DISTANCE:
            speed *= magnitude / CLOSE_DISTANCE  # scale down speed when very close to ball

        normalized_direction_x = direction_to_ball_x / magnitude
        normalized_direction_y = direction_to_ball_y / magnitude

        # Update the position based on speed and direction
        new_x = self.position[0] + normalized_direction_x * speed
        new_y = self.position[1] + normalized_direction_y * speed

        field_radius = 60  # assuming the playing field is a bit larger than the largest green
        distance_from_center = ((new_x**2) + (new_y**2))**0.5
        if distance_from_center > field_radius:
            scaling_factor = field_radius / distance_from_center
            new_x *= scaling_factor
            new_y *= scaling_factor

        self.position = (new_x, new_y)