import math
import time
import os
import logging

class Ball:
    def __init__(self, x, y, radius, mass, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.acceleration_y = 9.81  # gravity, negative as it's pulling the ball downwards

    def move(self, delta_time):
        """Update position of the ball based on its velocity."""
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time

        # Apply gravity
        self.velocity_y += self.acceleration_y * delta_time


    def collide_with_ball(self, other_ball):
        """Handle collision with another ball. Elastic collision formula is applied here."""
        dx = self.x - other_ball.x
        dy = self.y - other_ball.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= (self.radius + other_ball.radius):  # Collision detected
            angle = math.atan2(dy, dx)
            sin = math.sin(angle)
            cos = math.cos(angle)

            # Rotate ball's position
            pos0 = [0, 0]
            pos1 = [dx * cos + dy * sin, dy * cos - dx * sin]

            # Rotate ball's velocity
            v0 = [self.velocity_x * cos + self.velocity_y * sin,
                  self.velocity_y * cos - self.velocity_x * sin]
            v1 = [other_ball.velocity_x * cos + other_ball.velocity_y * sin,
                  other_ball.velocity_y * cos - other_ball.velocity_x * sin]

            # Collision reaction (1D elastic collision formulas)
            v_total = v0[0] - v1[0]
            v0[0] = ((self.mass - other_ball.mass) * v0[0] + 2 * other_ball.mass * v1[0]) / (self.mass + other_ball.mass)
            v1[0] = v0[0] + v_total

            # Rotate back
            final_v0 = [v0[0] * cos - v0[1] * sin, v0[1] * cos + v0[0] * sin]
            final_v1 = [v1[0] * cos - v1[1] * sin, v1[1] * cos + v1[0] * sin]

            self.velocity_x = final_v0[0]
            self.velocity_y = final_v0[1]
            other_ball.velocity_x = final_v1[0]
            other_ball.velocity_y = final_v1[1]

            # Correct positions to prevent overlap (simple method: move to the point of contact)
            overlap = 0.5 * (distance - self.radius - other_ball.radius)
            self.x -= overlap * (self.x - other_ball.x) / distance
            self.y -= overlap * (self.y - other_ball.y) / distance
            other_ball.x += overlap * (self.x - other_ball.x) / distance
            other_ball.y += overlap * (self.y - other_ball.y) / distance
    
    def collide_with_wall(self, x1, y1, x2, y2):
        """Handle collisions with the boundary walls."""
        if self.x - self.radius < x1 or self.x + self.radius > x2:
            self.velocity_x = -self.velocity_x  # Reflect ball's x velocity if hit vertical walls
        
        if self.y - self.radius < y1 or self.y + self.radius > y2:
            self.velocity_y = -self.velocity_y  # Reflect ball's y velocity if hit horizontal walls