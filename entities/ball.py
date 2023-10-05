import pygame
import math

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.z = 0  # Adding the z-coordinate for height
        self.radius = radius
        self.velocity = [1, 1, 10]  # Added a z-velocity
        self.on_green = False
        self.green = None
        self.last_team = None

    def update(self, greens):
        # Update the position of the ball based on its velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.z += self.velocity[2]

        # Apply gravity when the ball is in the air
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
        
        # Check for collisions with the greens
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

        # Check for collisions with the walls
        if self.x - self.radius < 0 or self.x + self.radius > 1920:
            self.velocity[0] = -self.velocity[0]
        if self.y - self.radius < 0 or self.y + self.radius > 1080:
            self.velocity[1] = -self.velocity[1]

    def draw(self, surface):
        # Adjust the radius of the ball based on its z value using a linear factor and a slight curve.
        growth_factor = self.z/20 + (math.pow(self.z, 1/2) / 10)  # Combine linear growth with cube root for a smoother transition
        adjusted_radius = self.radius + int(growth_factor)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), adjusted_radius)