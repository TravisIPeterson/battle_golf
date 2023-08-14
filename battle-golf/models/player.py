import random
import numpy as np
import math

class Player:
    MAX_SPEED = 20  # Maximum speed a player can achieve

    def __init__(self, role, stats=None):
        self.role = role
        self.stats = stats if stats else {
            key: random.randint(1, 20) for key in [
                'Power', 'Accuracy', 'Speed', 'Visual Calculus', 'Balance', 
                'Solidity', 'Savagery', 'Competitiveness', 'Cowardice', 'Neoliberalism',
                'Integrity'
            ]
        }
        self.position = (0, 0)
        self.green_number = random.randint(1, 8)

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
        # Assuming ball_position is a tuple where the first value is the green number
        ball_green = ball_position[0]
        decision = False
        
        # Check if the ball is on the same green as the player
        if ball_green == self.green_number:
            # Further logic (if any) for when the player should go for the ball
            decision = True

        if decision:
            print(random.choice([f"{self.role.capitalize()} decided to go for the ball!",
                                 f"{self.role.capitalize()} is making a move towards the ball!",
                                 f"Watch out! The {self.role} is on the move!"]))
        else:
            print(random.choice([f"{self.role.capitalize()} chose to stay put.",
                                 f"{self.role.capitalize()} is playing it safe.",
                                 f"Seems like the {self.role} is biding their time."]))

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

        selected_green = np.random.choice(greens, p=probabilities)
        print(random.choice([f"{self.role.capitalize()} is aiming for Green {selected_green}.",
                             f"Looks like Green {selected_green} is the target!",
                             f"{self.role.capitalize()} has Green {selected_green} in sight."]))
        return selected_green

    def drive(self, target_green_number, rival_green_number):
        # Calculate the power and accuracy for the drive
        power = self.stats['Power'] * random.uniform(0.9, 1.1)
        accuracy = self.stats['Accuracy'] * random.uniform(0.9, 1.1)

        # Calculate the rivalry intensity based on proximity to the rival's green
        green_difference = abs(target_green_number - rival_green_number)
        if green_difference == 0:
            rivalry_intensity = 1  # Maximum intensity when targeting the rival's green directly
        else:
            rivalry_intensity = 1.0 / green_difference

        # Modify power and accuracy based on competitiveness and rivalry intensity
        competitiveness = self.stats['Competitiveness'] * random.uniform(0.9, 1.1)
        competitive_boost = 1 + (competitiveness / 20.0 * rivalry_intensity)
        power *= competitive_boost
        accuracy *= competitive_boost

        # Check if the drive is successful based on the stats and random variability
        if power > random.uniform(17, 20) and accuracy > random.uniform(17, 20): #Successful Drive
            print(random.choice([f"Successful drive by the {self.role}! Ball landed on Green {target_green}.",
                                 f"{self.role.capitalize()} made an excellent shot to Green {target_green}.",
                                 f"Bravo! The ball made it to Green {target_green} thanks to the {self.role}."]))
            return target_green_number  

        # Determine the type of failure
        if power <= random.uniform(15, 18):  # Power failure
            greens = list(range(1, 9))
            probabilities = [1 / (abs(green - target_green_number) + 1e-10) for green in greens]  # Add a small constant to prevent division by zero
            total = sum(probabilities)
            if total == 0:  # This ensures that we don't encounter a situation where probabilities are all zeros.
                return random.choice(greens)  # In this unlikely scenario, choose a random green
            probabilities = [p / total for p in probabilities]  # Normalize probabilities
            failed_green = np.random.choice(greens, p=probabilities)
            return failed_green
        else:  # Accuracy failure
            return None  # Ball does not land on any green


    def block(self, ball):
        success = False
        # Calculate the relative speed of the player
        speed = self.stats['Speed'] * random.uniform(0.9, 1.1)

        # Factor in Visual Calculus
        visual_calculus_factor = self.stats['Visual Calculus'] / 20.0  # normalized to [0.05, 1]
        reaction_factor = speed * visual_calculus_factor  # Higher values mean faster reactions

        # Factor in Solidity and Cowardice for the block success
        solidity_factor = self.stats['Solidity'] / 20.0
        cowardice_penalty = self.stats['Cowardice'] / 20.0  # Higher cowardice reduces the player's blocking capability
        block_factor = solidity_factor * (1 - cowardice_penalty)

        # Combine the reaction and block factors to get overall blocking capability
        overall_block_capability = reaction_factor * block_factor

        # Determine success based on the overall capability vs. a random threshold (can be adjusted)
        BLOCK_THRESHOLD = random.uniform(0.5, 1)  # The higher the threshold, the harder it is to block
        if overall_block_capability > BLOCK_THRESHOLD:
            ball.position = self.position  # If using a ball class, update the ball's position to be with the blocker
            success = True  # block is successful
        if success:
            print(random.choice([f"Amazing block by the {self.role}!",
                                 f"{self.role.capitalize()} successfully blocked the ball.",
                                 f"The ball was stopped in its tracks by the {self.role}."]))
        else:
            print(random.choice([f"The {self.role} tried but missed the block.",
                                 f"Unfortunately, {self.role.capitalize()} couldn't stop the ball.",
                                 f"{self.role.capitalize()} failed to intercept."]))
        return success

    def aimed_shot(self, greens, players):
        num_greens = len(greens)
        greens_probabilities = [1 / float(num_greens)] * num_greens

        rival_green = (self.green_number + num_greens // 2 - 1) % num_greens + 1
        competitiveness_factor = (self.stats['Competitiveness'] - 10) / 10.0
        greens_probabilities[rival_green - 1] += competitiveness_factor * 0.1

        # Normalize probabilities
        total = sum(greens_probabilities)
        greens_probabilities = [p / total for p in greens_probabilities]

        # Adjust for rounding discrepancies
        discrepancy = 1.0 - sum(greens_probabilities)
        greens_probabilities[-1] += discrepancy

        # Safety check
        if not math.isclose(sum(greens_probabilities), 1.0, abs_tol=1e-10):
            raise ValueError("Probabilities do not sum up to 1.")

        chosen_green = np.random.choice(greens, p=greens_probabilities)

        # Determine if the player aims for the hole or another player based on savagery
        aim_for_player = random.random() < (self.stats['Savagery'] / 20.0)

        if aim_for_player:
            # Choose a player to target
            targeted_player = random.choice(players)
            print(random.choice([f"{self.role.capitalize()} is aiming for a player on Green {chosen_green}!",
                                 f"Watch out! {self.role.capitalize()} has a player in their sights on Green {chosen_green}.",
                                 f"A sneaky shot aimed at a player on Green {chosen_green} by the {self.role}."]))

            return targeted_player.green_number, aim_for_player
        else:
            print(random.choice([f"{self.role.capitalize()} decided to aim for Green {chosen_green}.",
                                 f"The ball is flying towards Green {chosen_green}!",
                                 f"{self.role.capitalize()} has sent the ball towards Green {chosen_green}."]))
            return chosen_green, aim_for_player
        
    def save(self, ball):
        save_prob = self.calculate_save_probability(ball.speed, ball.direction)

        if random.random() < save_prob:
            ball.green_number = self.green_number
            print(random.choice([f"Stunning save by the {self.role}!",
                                 f"{self.role.capitalize()} denied that shot with style!",
                                 f"A top-class save from the {self.role}."]))
        else:
            print(random.choice([f"Oh dear, the {self.role} missed the save.",
                                 f"{self.role.capitalize()} couldn't stop that one.",
                                 f"The ball got past the {self.role}."]))

        if self.stats['Balance'] < random.random():
            self.attempt_leap()
            self.fall_into_hole()

        return False

    def calculate_save_probability(self, ball_speed, ball_direction):
        speed_factor = self.stats['Speed'] / 100.0
        reaction_factor = (100 - self.stats['Visual Calculus']) / 100.0
        solidity_factor = self.stats['Solidity'] / 100.0
        balance_factor = self.stats['Balance'] / 100.0

        # You can adjust these weights if you want certain factors to be more impactful
        save_prob = 0.25 * speed_factor + 0.25 * reaction_factor + 0.25 * solidity_factor + 0.25 * balance_factor

        return save_prob

    def attempt_leap(self):
        leap_prob = (self.stats['Speed'] + self.stats['Balance'] + self.stats['Competitiveness']) / 300.0
        print(f"{self.role.capitalize()} attempts to leap over the hole...")

        if leap_prob > np.random.rand():
            print(f"...and makes it!")

        else:
            self.fall_into_hole()

    def fall_into_hole(self):
        print(random.choice([f"Oh no! {self.role.capitalize()} fell into a hole.",
                             f"A misstep! The {self.role} has fallen down.",
                             f"Disaster! {self.role.capitalize()} is in a hole now."]))

    def neoliberal_agenda(self, players):
        bribe_attempt_chance = self.stats['Neoliberalism'] / 20.0

        if random.random() < bribe_attempt_chance:
            potential_bribe_target = random.choice(players)
            bribe_resistance = (potential_bribe_target.stats['Integrity'] + potential_bribe_target.stats['Competitiveness']) / 40.0

            if bribe_attempt_chance / bribe_resistance > random.random():
                for stat, value in potential_bribe_target.stats.items():
                    potential_bribe_target.stats[stat] = int(value * 0.9)
                print(random.choice([f"{self.role.capitalize()} is trying to bribe the other players.",
                                 f"Looks like {self.role} has some tricks up their sleeve!",
                                 f"Watch out! The {self.role} is attempting to influence the game."]))
            else:
                print(random.choice([f"{self.role.capitalize()} is playing it fair and square.",
                                 f"No shady business from the {self.role} today.",
                                 f"{self.role.capitalize()} believes in a fair game."]))
        else:
            print(f"{self.role} chose not to bribe another player.")
