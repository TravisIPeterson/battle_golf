import pygame
import sys
import math
import random
sys.path.append('..')
from entities.green import Green
from entities.ball import Ball
from utils.constants import *
from entities.wall import Wall
from entities.wind import Wind

def random_point_inside_circle(cx, cy, r):
    theta = random.uniform(0, 2 * math.pi)  # Random angle
    distance_from_center = random.uniform(0, r)  # Random distance from center
    x = cx + distance_from_center * math.cos(theta)
    y = cy + distance_from_center * math.sin(theta)
    return x, y

# Initialize Pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('My Game')

# Set up the clock
clock = pygame.time.Clock()

# Calculate the positions of the greens in a circle
num_greens = 8
radius = 400
center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
angle_step = 2 * math.pi / num_greens

greens = []
for i in range(num_greens):
    angle = i * angle_step
    x = center[0] + radius * math.cos(angle)
    y = center[1] + radius * math.sin(angle)
    green = Green(team=f'Team {i}', x=x, y=y, radius=100, hole_x=x, hole_y=y)
    greens.append(green)

# Define the size of the square field and the zoom level
FIELD_SIZE = 100
ZOOM_LEVEL = 3

# Define the color of the border
BORDER_COLOR = (255, 255, 255)

# Create the Wall object
wall = Wall(greens)

# Create the Ball objects
num_balls = 8
balls = []

wind = Wind()

for i in range(num_balls):
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    safe_radius = wall.radius * 0.9
    start_x, start_y = random_point_inside_circle(center_x, center_y, safe_radius)
    ball = Ball(start_x, start_y, 2, wall, wind)
    balls.append(ball)

current_wind_speed = 0
current_wind_direction = 0

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(SKY_COLOR)

    # Draw the greens
    for green in greens:
        pygame.draw.circle(screen, GREEN_COLOR, (int(green.x), int(green.y)), int(green.radius))
        pygame.draw.circle(screen, BLACK_COLOR, (int(green.hole_x), int(green.hole_y)), int(green.radius * 0.015))

    wind.update()

    # Update and draw the ball objects
    for ball in balls:
        ball.update(greens)
        ball.draw(screen)

    # Draw the wall
    wall.draw(screen)

    # Get the position of the cursor
    cursor_pos = pygame.mouse.get_pos()

    # Calculate the coordinates of the top-left corner of the square field
    field_x = cursor_pos[0] - FIELD_SIZE // 2
    field_y = cursor_pos[1] - FIELD_SIZE // 2

    # Create a new surface with the size of the square field and blit the portion of the screen that corresponds to the square field onto it
    field_surface = pygame.Surface((FIELD_SIZE, FIELD_SIZE))
    field_surface.blit(screen, (-field_x, -field_y))

    # Draw the border around the field
    pygame.draw.rect(field_surface, BORDER_COLOR, pygame.Rect(0, 0, FIELD_SIZE, FIELD_SIZE), 1)

    # Scale the new surface based on the zoom level
    zoomed_surface = pygame.transform.scale(field_surface, (FIELD_SIZE * ZOOM_LEVEL, FIELD_SIZE * ZOOM_LEVEL))

    # Blit the scaled surface onto the corner of the screen
    screen.blit(zoomed_surface, (0, 0))

    # Draw the border around the cursor
    pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(cursor_pos[0] - FIELD_SIZE // 2 - 1, cursor_pos[1] - FIELD_SIZE // 2 - 1, FIELD_SIZE + 2, FIELD_SIZE + 2), 1)

    # Draw the wind direction and speed indicator
    wind_speed_text = FONT.render(str(round(balls[0].wind.speed)), True, TEXT_COLOR)
    screen.blit(wind_speed_text, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50))

    # Map wind direction to arrow rotation
    direction_angles = {
        "N": 0,
        "NE": 45,
        "E": 90,
        "SE": 135,
        "S": 180,
        "SW": 225,
        "W": 270,
        "NW": 315
    }
    angle = direction_angles[balls[0].wind.direction]

    # Create a new surface for the wind direction arrow
    wind_direction_arrow = pygame.Surface((50, 50), pygame.SRCALPHA)

    # Draw the arrow shape on the wind direction arrow surface
    pygame.draw.polygon(wind_direction_arrow, TEXT_COLOR, [(25, 5), (5, 45), (25, 35), (45, 45)], 0)

    # Rotate the wind direction arrow surface by the wind direction angle
    rotated_arrow = pygame.transform.rotate(wind_direction_arrow, -angle)

    # Blit the wind direction arrow onto the screen
    arrow_pos = (SCREEN_WIDTH - 75, SCREEN_HEIGHT - 225)
    screen.blit(rotated_arrow, arrow_pos)

    # Display the direction text below the arrow
    direction_text = FONT.render(balls[0].wind.direction, True, TEXT_COLOR)
    screen.blit(direction_text, (SCREEN_WIDTH - 65, SCREEN_HEIGHT - 180))

    # Update the screen
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

    if not current_wind_speed == balls[0].wind.speed:
        print(f"Wind speed: {balls[0].wind.speed}")
        current_wind_speed = balls[0].wind.speed
    if not current_wind_direction == balls[0].wind.direction:
        print(f"Wind direction: {balls[0].wind.direction}")
        current_wind_direction = balls[0].wind.direction