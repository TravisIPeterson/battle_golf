import random

class DefensiveActions:

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
            ball.green_number = self.green_number  # If using a ball class, update the ball's position to be with the blocker
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

    def save(self):
        # Calculate save probability
        speed_factor = self.stats['Speed'] / 100.0
        reaction_factor = (100 - self.stats['Visual Calculus']) / 100.0
        solidity_factor = self.stats['Solidity'] / 100.0
        balance_factor = self.stats['Balance'] / 100.0

        # You can adjust these weights if you want certain factors to be more impactful
        save_prob = 0.25 * speed_factor + 0.25 * reaction_factor + 0.25 * solidity_factor + 0.25 * balance_factor

        # Decide save outcome
        if random.random() < save_prob:
            print(random.choice([f"Stunning save by the {self.role}!",
                                f"{self.role.capitalize()} denied that shot with style!",
                                f"A top-class save from the {self.role}."]))
        else:
            print(random.choice([f"Oh dear, the {self.role} missed the save.",
                                f"{self.role.capitalize()} couldn't stop that one.",
                                f"The ball got past the {self.role}."]))

        # Check for potential fall into hole
        if self.stats['Balance'] < random.random():
            self.attempt_leap()
            self.fall_into_hole()

        return False
    
    def attempt_leap(self):
        leap_prob = (self.stats['Speed'] + self.stats['Balance'] + self.stats['Competitiveness']) / 300.0
        print(f"{self.role.capitalize()} attempts to leap...")

        if leap_prob > np.random.rand():
            print(f"...and makes it!")
        else:
            self.fall_into_hole()

    def fall_into_hole(self):
        print(random.choice([f"Oh no! {self.role.capitalize()} fell.",
                            f"A misstep! The {self.role} has fallen.",
                            f"Disaster! {self.role.capitalize()} is down."]))