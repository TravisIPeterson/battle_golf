import random

first_names = ['Scoot', 'Crime', 'Hoss', 'Benjamina', 'Breery', 'Kermit', 'Horse', 'Scout', 'Jimothy', 'Kimothy', 'Vera', 'Hades', 'Georgio', 'Jordi', 'Athena', 'Cordelia', 'William']
last_names = ['McGee', 'McGoo', 'McGuffin', 'Briner', 'Brelinda', 'Manman', 'Mann', 'Mannly', 'Mannman', 'Mannwoman', 'Mannchild', 'Aaronson', 'Badly', 'Baddington', 'Broomhilda', 'Watkins']
              
class Player:
    def __init__(self, position):
        self.position = position
        self.stats = {
            'Power': random.uniform(1.0, 10.0),
            'Accuracy': random.uniform(1.0, 10.0),
            'Speed': random.uniform(1.0, 10.0),
            'Visual Calculus': random.uniform(1.0, 10.0),
            'Balance': random.uniform(1.0, 10.0),
            'Solidity': random.uniform(1.0, 10.0),
            'Savagery': random.uniform(1.0, 10.0),
            'Competitiveness': random.uniform(1.0, 10.0),
            'Cowardice': random.uniform(1.0, 10.0),
            'Neoliberalism': random.uniform(1.0, 10.0),
            'Integrity': random.uniform(1.0, 10.0),
            'Goutiness': random.uniform(1.0, 10.0)
        }
        self.weighted_stats()

    def generate_name(self):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        return f"{first_name} {last_name}"

    def weighted_stats(self):
        for stat in self.stats:
            weight = random.uniform(0.5, 1.5)
            if self.position == 'shooter':
                weight += random.uniform(0.0, 0.5)
                if stat == 'Power' or stat == 'Accuracy':
                    weight += random.uniform(0.5, 1.0)
            elif self.position == 'blocker':
                weight += random.uniform(-0.5, 0.0)
                if stat == 'Balance' or stat == 'Solidity' or stat == 'Savagery':
                    weight += random.uniform(0.5, 1.0)
            elif self.position == 'marksman':
                weight += random.uniform(0.0, 0.5)
                if stat == 'Accuracy':
                    weight += random.uniform(0.5, 1.0)
            elif self.position == 'goalie':
                weight += random.uniform(-0.5, 0.0)
                if stat == 'Visual Calculus':
                    weight += random.uniform(0.5, 1.0)
            self.stats[stat] *= weight