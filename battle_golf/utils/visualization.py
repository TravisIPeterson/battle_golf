import pygame
import sys
from entities.green import Green as greens

# Initialize Pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('My Game')

# Set up the clock
clock = pygame.time.Clock()

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the greens
    for green in greens:
        pygame.draw.circle(screen, (0, 255, 0), (int(green.x), int(green.y)), int(green.radius))

    # Update the screen
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)