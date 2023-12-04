import pygame
import random

class Wind:
    def __init__(self):
        self.speed = random.uniform(0, 10)  # Initialize with a random speed between 0 and 10
        self.direction = random.choice(["N", "S", "E", "W", "NE", "NW", "SE", "SW"])
        self.last_update_time = pygame.time.get_ticks()  # Record the current time
        self.last_strong_gust_time = None  # Time since a strong gust was initiated
        self.update_interval = 10000  # 10 seconds in milliseconds
        self.strong_gust_duration = 5000  # 5 seconds in milliseconds

        if self.speed > 5:
            self.last_strong_gust_time = pygame.time.get_ticks()
    
    def update(self):
        current_time = pygame.time.get_ticks()

        # Check if it's time to tone down a strong gust
        if (self.last_strong_gust_time and current_time - self.last_strong_gust_time >= self.strong_gust_duration and self.speed > 5):  # Check if the speed is above 5 for a strong gust
            self.speed = random.uniform(0, 5)  # Reduce the speed
            self.last_strong_gust_time = None  # Reset the gust time so we don't keep reducing

        # Check if it's time to change wind speed and direction
        if current_time - self.last_update_time >= self.update_interval:
            self.last_update_time = current_time  # Reset the timer

            # Intermittently update the speed
            if random.random() < 0.5:  # 50% chance every 10 seconds
                self.speed += random.uniform(-1, 1)

            # Small chance of drastic change in speed
            if random.random() < 0.05:  # 5% chance every 10 seconds
                previous_speed = self.speed
                self.speed += random.uniform(-4, 4)
                
                if abs(self.speed) > 7 and abs(self.speed - previous_speed) > 4:  # Check for strong gust
                    self.last_strong_gust_time = current_time  # Record the time of the strong gust

                    # Change the wind direction
                    adj_directions = {
                        "N": ["NW", "NE"],
                        "S": ["SW", "SE"],
                        "E": ["NE", "SE"],
                        "W": ["NW", "SW"],
                        "NE": ["N", "E"],
                        "NW": ["N", "W"],
                        "SE": ["S", "E"],
                        "SW": ["S", "W"]
                    }
                    self.direction = random.choice(adj_directions[self.direction])

            # Cap wind speed between 0 and 10
            self.speed = max(0, min(10, self.speed))


    def effect_on_ball(self, height_multiplier):
        effect = self.speed * height_multiplier * 0.01
        return (effect, self.direction)
    
    def get_direction_vector(self):
        direction_vectors = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0),
            "NE": (1, -1),
            "NW": (-1, -1),
            "SE": (1, 1),
            "SW": (-1, 1)
        }
        return direction_vectors[self.direction], self.speed