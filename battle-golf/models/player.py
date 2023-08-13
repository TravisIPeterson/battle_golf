import random
import numpy as np
from .ball import Ball

class Player:
    MAX_SPEED = 20  # Maximum speed a player can achieve
    GREEN_BOUNDARY = 100  # define the boundary of the green

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
        self.green_boundary = GREEN_BOUNDARY
        self.center_position = (0, 0)
    
    def normalize_vector(self, vector):
        """Return a normalized version of a 2D vector."""
        magnitude = (vector[0]**2 + vector[1]**2)**0.5
        if magnitude == 0:  # Avoid dividing by zero
            return (0, 0)
        return (vector[0]/magnitude, vector[1]/magnitude)

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

    def should_go_for_ball(self, ball_position):
        distance_to_ball = np.linalg.norm(np.array(ball_position) - np.array(self.position))
        desire_factor = self.stats['Speed'] * self.stats['Competitiveness'] / 400.0  # just a derived metric
        
        if self.role in ["driver", "marksman"]:
            threshold_distance = 20 * (1 - desire_factor)  # same as before
            return distance_to_ball < threshold_distance

        elif self.role == "blocker":
            pursue_threshold = 15
            defend_boundary = 5
            if ball_position[0] > self.green_boundary - defend_boundary:
                return False
            return distance_to_ball < pursue_threshold

        elif self.role == "goalie":
            goalie_move_boundary = 20
            danger_zone = 10

            if np.linalg.norm(np.array(self.position) - np.array(self.center_position)) < danger_zone:
                repelling_force = (danger_zone - distance_to_center) / danger_zone
                if distance_to_ball * repelling_force < 5:  # Threshold to decide if goalie should take the risk
                    return True
                return False
                
            if np.linalg.norm(np.array(self.position) - np.array(self.center_position)) < goalie_move_boundary:
                return True

        return False

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

        # Ensure ball doesn't exceed the green's boundary
        landing_x = max(-10, min(10, landing_x))
        landing_y = max(-10, min(10, landing_y))

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
        speed = self.calculate_speed()
        direction_to_ball = (ball_position[0] - self.position[0], ball_position[1] - self.position[1])
        normalized_direction = self.normalize_vector(direction_to_ball)

        # Factor in balance on the sloped green
        balance_factor = self.stats['Balance'] / 20.0  # normalize to [0.05, 1]
        speed *= balance_factor

        # Add competitiveness boost
        competitiveness_boost = (self.stats['Competitiveness'] - 10) / 100.0  # results in [-0.1, 0.1]
        speed += speed * competitiveness_boost

        # Cap the max speed
        MAX_SPEED = 20  # Arbitrarily chosen, you can modify based on your needs
        speed = min(speed, MAX_SPEED)

        # Calculate the new position after movement
        delta_x = normalized_direction[0] * speed
        delta_y = normalized_direction[1] * speed
        new_position = (self.position[0] + delta_x, self.position[1] + delta_y)

        # Ensure player doesn't overshoot the ball. If the player's next position would place them past the ball, 
        # set their position to the ball's position.
        future_distance_to_ball = np.linalg.norm(np.array(new_position) - np.array(ball_position))
        if future_distance_to_ball < speed:
            new_position = ball_position

        # Update the player's position
        self.position = new_position

        return new_position

    def attempt_leap(self, ball_position):
        danger_zone = 10
        distance_to_center = np.linalg.norm(np.array(self.position) - np.array(self.center_position))
        
        if distance_to_center < danger_zone:
            leap_distance = (self.stats['Speed'] + self.stats['Balance'] + self.stats['Competitiveness']) / 30
            
            if np.linalg.norm(np.array(ball_position) - np.array(self.position)) < danger_zone:
                direction = np.array(ball_position) - np.array(self.position)
            else:
                direction = np.array(self.position) - np.array(self.center_position)

            direction_normalized = direction / np.linalg.norm(direction)
            new_position = np.array(self.position) + direction_normalized * leap_distance

            success_chance = (self.stats['Visual Calculus'] + self.stats['Balance']) / 20

            if success_chance > np.random.rand():
                self.position = new_position.tolist()
                return True  # Successful leap

        return False  # Unsuccessful leap or not in danger zone

    def fall_into_hole(self):
        """Handle the logic when the player falls into the hole."""
        # This function can be expanded depending on the game mechanics.
        # For instance, you could deduct points, remove the player from the game for a duration, etc.
        # As an example:
        print(f"{self.role} has fallen into the hole!")
        # Reset player's position to the starting point or a safe point
        self.position = (0, 0)

    def neoliberal_agenda(self, players):
    """A function for the 'Neoliberalism' stat. It can represent any game mechanic 
    where the player may have an advantage/disadvantage based on economic strategy or relationships.
    This is just a humorous addition and can be interpreted in multiple ways."""

    # For simplicity, a player with a higher Neoliberalism stat might have a chance to 'bribe' other players
    # and make them perform worse temporarily. 
    bribe_success_chance = self.stats['Neoliberalism'] / 20.0  # normalized to [0.05, 1]

    if random.random() < bribe_success_chance:
        # Choose a player to bribe; in a more refined version, this could consider player positions, roles, etc.
        bribed_player = random.choice(players)
        
        # Reduce the bribed player's stats temporarily. The mechanics of how and when to restore them is up to you.
        for stat, value in bribed_player.stats.items():
            bribed_player.stats[stat] = int(value * 0.9)  # Reducing each stat by 10%

        print(f"{self.role} has successfully bribed {bribed_player.role}!")

    else:
        print(f"{self.role} failed to bribe another player!")