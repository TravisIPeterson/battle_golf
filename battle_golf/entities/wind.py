import random
import math

class Wind:
    def __init__(self, speed=0, direction=0):
        self.speed = speed
        self.direction = direction

    def update(self):
        # Update the wind speed and direction randomly
        if random.random() < 0.01:
            # Very rarely have a sudden huge change in speed and direction
            self.speed *= random.uniform(0, 5)
            self.direction = random.uniform(0, 2 * math.pi)
        elif random.random() < 0.1:
            # Change the wind speed and direction slightly every few minutes
            self.speed += random.uniform(-3, 3)
            self.direction += random.uniform(-0.1, 0.1)
        else:
            # No change in wind speed and direction
            pass

        # Clamp the wind speed and direction to valid ranges
        self.speed = max(0, min(self.speed, 50))
        self.direction = self.direction % (2 * math.pi)

    def get_speed(self):
        # Get the current wind speed
        return self.speed

    def get_direction(self):
        # Get the current wind direction
        return self.direction