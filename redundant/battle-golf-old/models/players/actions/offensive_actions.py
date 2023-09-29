import random
import numpy as np

class OffensiveActions:

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

    def aimed_shot(self, greens):
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

        print(random.choice([f"{self.role.capitalize()} decided to aim for Green {chosen_green}.",
                            f"The ball is flying towards Green {chosen_green}!",
                            f"{self.role.capitalize()} has sent the ball towards Green {chosen_green}."]))

        return chosen_green