import pygame
import math
import random
from entities.wind import Wind
from entities.wall import Wall
from game_logic.game_state import Coordinates

class Ball:
    def __init__(self, x, y, radius, wall, wind):
        self.coordinates = Coordinates(x, y, 0)
        self.radius = radius
        self.velocity = [1, 1, 10]
        self.on_green = False
        self.green = None
        self.last_team = None
        self.time_in_air = 0
        self.wind = wind
        self.time_on_ground = 0
        self.wall = wall
    
    @property
    def x(self):
        return self.coordinates.x
    
    @x.setter
    def x(self, value):
        self.coordinates.x = value

    @property
    def y(self):
        return self.coordinates.y
    
    @y.setter
    def y(self, value):
        self.coordinates.y = value

    @property
    def z(self):
        return self.coordinates.z
    
    @z.setter
    def z(self, value):
        self.coordinates.z = value

    def update(self, greens):

        # Calculate wind effect based on height (z value) of the ball
        # Assuming the ball's max height can be 100 for full effect; adjust this value as necessary
        max_height_for_full_effect = 100
        wind_effect_multiplier = self.z / max_height_for_full_effect
        wind_effect = self.wind.effect_on_ball(wind_effect_multiplier)
        wind_effect = [wind_effect[0] * 0.2, wind_effect[1]]  # Reduce the effect of the wind
            
        # Convert wind direction to x, y velocity components based on compass direction
        wind_effects = self.get_wind_effects(wind_effect)
        
        self.velocity[0] += wind_effects[self.wind.direction][0]
        self.velocity[1] += wind_effects[self.wind.direction][1]

        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.z += self.velocity[2]

        self.calculate_air_time()
        self.check_wall_collision()
        self.handle_ground_collisions()

        # Check if ball is on a green
        self.check_green_collisions(greens)

    def get_wind_effects(self, wind_effect):
        return {
            "N": (0, -wind_effect[0]),
            "S": (0, wind_effect[0]),
            "E": (wind_effect[0], 0),
            "W": (-wind_effect[0], 0),
            "NE": (wind_effect[0]/math.sqrt(2), -wind_effect[0]/math.sqrt(2)),
            "NW": (-wind_effect[0]/math.sqrt(2), -wind_effect[0]/math.sqrt(2)),
            "SE": (wind_effect[0]/math.sqrt(2), wind_effect[0]/math.sqrt(2)),
            "SW": (-wind_effect[0]/math.sqrt(2), wind_effect[0]/math.sqrt(2)),
        }

    def check_green_collisions(self, greens):
        on_green = False
        green = None
        for g in greens:
            distance = math.sqrt((self.x - g.x) ** 2 + (self.y - g.y) ** 2)
            if distance < g.radius:
                on_green = True
                green = g
                break
        self.on_green = on_green
        self.green = green
    
    def handle_ground_collisions(self):

        if self.z > 0:
            self.velocity[2] -= 0.1
        elif self.z <= 0:  # When the ball hits the ground
            self.z = 0  # Ensure the ball doesn't go below the ground
            if self.velocity[2] < 0:  # If the ball had a downward velocity
                self.velocity[2] = -self.velocity[2] * 0.3  # Bounce the ball, reducing its velocity
        
        if self.z == 0:
            friction_coefficient = 0.9  # You can adjust this value for more or less friction
            self.velocity[0] *= friction_coefficient
            self.velocity[1] *= friction_coefficient

        # If velocities are very small (below threshold), set them to 0 to stop the ball
        threshold_velocity = 0.01
        if abs(self.velocity[0]) < threshold_velocity:
            self.velocity[0] = 0
        if abs(self.velocity[1]) < threshold_velocity:
            self.velocity[1] = 0
        if abs(self.velocity[2]) < threshold_velocity:
            self.velocity[2] = 0

    def check_wall_collision(self):
        # Calculate distance between ball's center and the center of the circle
        distance_to_center = math.sqrt((self.x - self.wall.x)**2 + (self.y - self.wall.y)**2)

        # Check if the ball has collided with the boundary of the circle
        if distance_to_center >= self.wall.radius - self.radius:
            # Calculate the normal vector from the center of the circle to the ball's center
            normal_vector = [(self.wall.x - self.x) / distance_to_center, 
                            (self.wall.y - self.y) / distance_to_center]
            
            # Dot product between ball's velocity and normal vector
            dot_product = self.velocity[0]*normal_vector[0] + self.velocity[1]*normal_vector[1]
            
            # Reflect the ball's velocity across the normal
            self.velocity[0] -= 2 * dot_product * normal_vector[0]
            self.velocity[1] -= 2 * dot_product * normal_vector[1]

            # Add some friction or reduce ball's speed after the collision
            self.velocity[0] *= 0.9
            self.velocity[1] *= 0.9

            # Push the ball out of the circle to prevent it from getting stuck
            push_out_distance = self.radius - self.wall.radius + distance_to_center + 1  # +1 or a small number for a slight push
            self.x += push_out_distance * normal_vector[0]
            self.y += push_out_distance * normal_vector[1]

    
    def calculate_air_time(self):
        if self.z > 0:
            self.time_in_air += 1
        else:
            self.time_in_air = 0

    def draw(self, surface):
        # Adjust the radius of the ball based on its z value using a linear factor and a slight curve.
        growth_factor = self.z/20 + (math.pow(self.z, 1/2) / 10)  # Combine linear growth with cube root for a smoother transition
        adjusted_radius = self.radius + int(growth_factor)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), adjusted_radius)