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
from entities.team import Team
from game_logic.game_state import Coordinates
import math
import random
import time

teams = Team.get_teams_from_db('../teams/battle_golf.db')
balls = []

def random_point_inside_circle(cx, cy, r):
    theta = random.uniform(0, 2 * math.pi)  # Random angle
    distance_from_center = random.uniform(0, r)  # Random distance from center
    x = cx + distance_from_center * math.cos(theta)
    y = cy + distance_from_center * math.sin(theta)
    return x, y

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Battle Golf')
    clock = pygame.time.Clock()

    greens = create_greens(teams)
    players = place_players_on_greens(greens)
    wall = Wall(greens)
    wind = Wind()

    return screen, clock, greens, players, wall, wind, balls

def create_greens(teams):
    num_greens = len(teams)
    radius = 400
    center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    angle_step = 2 * math.pi / num_greens

    greens = []
    for i in range(num_greens):
        angle = i * angle_step
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        green = Green(team=teams[i].id, x=x, y=y, radius=100, hole_x=x, hole_y=y)
        print(green.team)
        greens.append(green)

    return greens

def place_players_on_greens(greens):
    def generate_players_within_green(green):
        return random_point_inside_circle(green.x, green.y, green.radius - 10)

    players = Player.get_players_from_db()
    for player in players:
        team = player.team_id
        corresponding_green = next(g for g in greens if g.team == team)
        x, y = generate_players_within_green(corresponding_green)
        player.coordinates = Coordinates(x, y)  # Set the coordinates directly as a Coordinates object
        player.target_coordinates = player.coordinates

    return players

def create_ball_count():
    total_balls = random.randint(150, 300)
    initial_drop_count = int(total_balls * random.uniform(0.15, 0.25))
    return total_balls, initial_drop_count

def drop_ball(wall, wind, balls):
    center_x = random.uniform(400, 1200)
    center_y = random.uniform(0, 1080)
    ball = Ball(center_x, center_y, 1, wall, wind)
    ball.coordinates.z = 500
    ball.velocity = [random.uniform(-5, 5), random.uniform(-5, 5), -2]
    balls.append(ball)

def main_game_loop():
    screen, clock, greens, players, wall, wind, balls = initialize_game()
    total_balls, initial_drop_count = create_ball_count()
    remaining_balls = total_balls
    balls = []
    last_ball_drop_time = time.time()
    initial_drop_done = False
    initial_drop_interval = random.uniform(5, 7) / initial_drop_count

    running = True
    while running:
        current_time = time.time()
        if not initial_drop_done:
            if current_time - last_ball_drop_time > initial_drop_interval and remaining_balls > 0:
                drop_ball(wall, wind, balls)
                remaining_balls -= 1
                last_ball_drop_time = current_time
                initial_drop_interval = random.random() * 0.1
                if remaining_balls == total_balls - initial_drop_count:
                    initial_drop_done = True
                    last_ball_drop_time = current_time
        else:
            if current_time - last_ball_drop_time > random.uniform(0, 20) and remaining_balls > 0:
                drop_ball(wall, wind, balls)
                remaining_balls -= 1
                last_ball_drop_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for ball in balls:
            if ball.in_hole == True:
                balls.remove(ball)
            else:
                ball.update(greens, teams)
                ball.check_player_collisions(players)
        choose_action(balls, players, greens, wind)
        draw_game_state(players, greens, balls, wall, wind, teams, screen, remaining_balls)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main_game_loop()
