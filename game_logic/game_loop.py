import pygame
import sys
sys.path.append('..')
from utils.visualization import draw_game_state, SCREEN_WIDTH, SCREEN_HEIGHT
from player_actions import choose_action
from entities.wall import Wall
from entities.wind import Wind
from entities.player import Player
from entities.green import Green
from entities.ball import Ball
import math
import random

def random_point_inside_circle(cx, cy, r):
    theta = random.uniform(0, 2 * math.pi)  # Random angle
    distance_from_center = random.uniform(0, r)  # Random distance from center
    x = cx + distance_from_center * math.cos(theta)
    y = cy + distance_from_center * math.sin(theta)
    return x, y

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Battle Golf')
    clock = pygame.time.Clock()

    greens = create_greens()
    players = place_players_on_greens(greens)
    wall = Wall(greens)
    wind = Wind()
    balls = create_balls(wall, wind)

    return screen, clock, greens, players, wall, wind, balls

def create_greens():
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

    return greens

def place_players_on_greens(greens):
    def generate_players_within_green(green):
        return random_point_inside_circle(green.x, green.y, green.radius - 10)

    players = Player.get_players_from_db()
    for player in players:
        team = player.team_id
        corresponding_green = next(g for g in greens if g.team == "Team " + str(team - 1))
        x, y = generate_players_within_green(corresponding_green)
        setattr(player, 'coordinates', (x, y))

    return players

def create_balls(wall, wind):
    num_balls = 8
    balls = []
    for i in range(num_balls):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        safe_radius = wall.radius * 0.9
        start_x, start_y = random_point_inside_circle(center_x, center_y, safe_radius)
        ball = Ball(start_x, start_y, 1.5, wall, wind)
        balls.append(ball)

    return balls

def main_game_loop():
    screen, clock, greens, players, wall, wind, balls = initialize_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        choose_action(balls, players)
        draw_game_state(players, greens, balls, wall, wind, screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main_game_loop()
