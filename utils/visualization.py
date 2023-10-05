import pygame
import sys
import math
sys.path.append('..')
from entities.green import Green
from entities.ball import Ball

# Initialize Pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('My Game')

# Set up the clock
clock = pygame.time.Clock()

# Calculate the positions of the greens in a circle
num_greens = 8
radius = 400
center = (960, 510)
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

# Create the ball object
ball = Ball(500, 500, 2)

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((50, 50, 50))

    # Draw the greens
    for green in greens:
        pygame.draw.circle(screen, (0, 255, 70), (int(green.x), int(green.y)), int(green.radius))
        pygame.draw.circle(screen, (0, 0, 0), (int(green.hole_x), int(green.hole_y)), int(green.radius * 0.015))

    # Update the ball object
    ball.update(greens)

    # Draw the ball object
    ball.draw(screen)

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

    # Update the screen
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

    print(ball.x, ball.y, ball.z, ball.velocity, ball.on_green, ball.green, ball.last_team)
    
    if ball.on_green:
        print(ball.green.team)