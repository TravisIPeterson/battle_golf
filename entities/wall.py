import pygame
import math

class Wall:
    def __init__(self, greens):
        # Calculate the center point and radius of the big circle
        x_values = [green.x for green in greens]
        y_values = [green.y for green in greens]
        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)
        center_x = (min_x + max_x) // 2
        center_y = (min_y + max_y) // 2

        # Use one of the greens to adjust the wall's radius so that it's drawn along the outer edge of the greens
        distance_to_first_green = math.sqrt((greens[0].x - center_x)**2 + (greens[0].y - center_y)**2)
        radius = distance_to_first_green + greens[0].radius

        self.x = center_x
        self.y = center_y
        self.radius = radius + 40
        self.thickness = 5

    def draw(self, screen):
        # Draw the wall as a circle with the calculated center point and radius
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius, self.thickness)