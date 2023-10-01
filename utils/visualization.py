import pygame
import sys
import math
sys.path.append('..')
from entities.green import Green

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
        pygame.draw.circle(screen, (0, 0, 0), (int(green.hole_x), int(green.hole_y)), int(green.radius * 0.1))

    # Update the screen
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)