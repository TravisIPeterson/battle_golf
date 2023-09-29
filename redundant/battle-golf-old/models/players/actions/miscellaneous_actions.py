import random

class MiscellaneousActions:

    def neoliberal_agenda(self, players):
        bribe_attempt_chance = self.stats['Neoliberalism'] / 20.0

        if random.random() < bribe_attempt_chance:
            potential_bribe_target = random.choice(players)
            bribe_resistance = (potential_bribe_target.stats['Integrity'] + potential_bribe_target.stats['Competitiveness']) / 40.0
            if bribe_resistance < 1:
                bribe_resistance = 1

            if bribe_attempt_chance / bribe_resistance > random.random():
                for stat, value in potential_bribe_target.stats.items():
                    potential_bribe_target.stats[stat] = int(value * 0.9)
                print(random.choice([f"{self.role.capitalize()} is trying to bribe other players.",
                                f"Looks like {self.role} has some tricks up their sleeve!",
                                f"Watch out! The {self.role} is attempting to influence the game."]))
            else:
                print(random.choice([f"{self.role.capitalize()} is playing it fair and square.",
                                f"No shady business from the {self.role} today.",
                                f"{self.role.capitalize()} believes in a fair game."]))
        else:
            print(f"{self.role} chose not to bribe another player.")