import pygame
import sys
sys.path.append('..')
from utils.constants import *

# Define the size of the square field and the zoom level
FIELD_SIZE = 100
ZOOM_LEVEL = 3

# Define the color of the border
BORDER_COLOR = (255, 255, 255)

TEAM_COLORS = {
    1: (255, 0, 0),
    2: (0, 255, 0),
    3: (0, 0, 255),
    4: (0, 255, 255),
    5: (255, 255, 0),
    6: (128, 128, 0),
    7: (255, 0, 255),
    8: (0, 128, 128)
}

def draw_game_state(players, greens, balls, wall, wind, teams, screen):
    # Clear the screen
    screen.fill(SKY_COLOR)

    draw_scores(screen, teams)

    # Draw the greens
    for green in greens:
        pygame.draw.circle(screen, GREEN_COLOR, (int(green.x), int(green.y)), int(green.radius))
        pygame.draw.circle(screen, BLACK_COLOR, (int(green.hole_x), int(green.hole_y)), int(green.radius * 0.05))

    # Draw players
    for player in players:
        x = player.coordinates.x
        y = player.coordinates.y
        pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 11)
        pygame.draw.circle(screen, TEAM_COLORS[player.team_id], (int(x), int(y)), 10)

        text_surface = PLAYER_FONT.render(player.initials, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    wind.update()

    # Update and draw the ball objects
    for ball in balls:
        ball.update(greens)
        ball.draw(screen)

    # Draw the wall
    wall.draw(screen)

    # Draw the wind direction and speed indicator
    wind_speed_text = WIND_FONT.render(str(round(balls[0].wind.speed)), True, TEXT_COLOR)
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
    direction_text = WIND_FONT.render(balls[0].wind.direction, True, TEXT_COLOR)
    screen.blit(direction_text, (SCREEN_WIDTH - 65, SCREEN_HEIGHT - 180))

def draw_scores(screen, teams):
    start_y = 20
    padding = 5

    for team in teams:
        team_color = TEAM_COLORS.get(team.id, (255, 255, 255))
        
        score_text = TEAM_FONT.render(f"{team.name}: {team.score}", True, team_color)
        screen.blit(score_text, (padding, start_y))
        start_y += score_text.get_height() + padding