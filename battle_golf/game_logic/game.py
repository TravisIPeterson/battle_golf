import random
import math
import sys
sys.path.append('..')
from teams.player import Player

class Game:
    def __init__(self, teams, ball, physics_engine):
        self.teams = teams
        self.ball = ball
        self.physics_engine = physics_engine

    def initialize(self):
        # Assign existing players to teams
        players = []
        for team in self.teams:
            for player in team.players:
                players.append(player)
        random.shuffle(players)
        for i, player in enumerate(players):
            team = self.teams[i % len(self.teams)]
            team.players.append(player)

        # Place the ball on a random green
        green = random.choice(self.greens)
        self.ball.position = (green.x, green.y)
        self.ball.on_green = green
        self.ball.green_owner = green.team

    def simulate_turn(self):
        # Move the ball according to the laws of physics and the effects of wind and obstacles
        time = 1  # Assume one second per turn for simplicity
        total_v_x, total_v_y, x, y, ground_angle = self.physics_engine.calculate_trajectory(self.ball.velocity, self.ball.angle, time, self.ball.on_ground, 0)
        self.ball.position = (self.ball.position[0] + x, self.ball.position[1] + y)
        self.ball.velocity = (total_v_x, total_v_y)

        # Check if the ball is on a green
        for green in self.greens:
            distance = math.sqrt((self.ball.position[0] - green.x) ** 2 + (self.ball.position[1] - green.y) ** 2)
            if distance <= green.radius:
                self.ball.on_green = green
                self.ball.green_owner = green.team
                break
        else:
            self.ball.on_green = None
            self.ball.green_owner = None

        # Check if the ball is in possession of a player
        if self.ball.in_possession:
            player = self.ball.possession_owner
            if player.role == 'driver':
                # Move the ball in the direction of the player's position
                dx = player.position[0] - self.ball.position[0]
                dy = player.position[1] - self.ball.position[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance > 0:
                    dx /= distance
                    dy /= distance
                self.ball.position = (self.ball.position[0] + dx, self.ball.position[1] + dy)
            elif player.role == 'blocker':
                # Move the ball away from the player's position
                dx = self.ball.position[0] - player.position[0]
                dy = self.ball.position[1] - player.position[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance > 0:
                    dx /= distance
                    dy /= distance
                self.ball.position = (self.ball.position[0] + dx, self.ball.position[1] + dy)
            elif player.role == 'marksman':
                # Move the ball towards the hole of the opposing team's green
                dx = self.ball.on_green.hole_x - self.ball.position[0]
                dy = self.ball.on_green.hole_y - self.ball.position[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance > 0:
                    dx /= distance
                    dy /= distance
                self.ball.position = (self.ball.position[0] + dx, self.ball.position[1] + dy)
            elif player.role == 'goalie':
                # Move the ball away from the team's own hole
                dx = self.ball.position[0] - self.ball.on_green.hole_x
                dy = self.ball.position[1] - self.ball.on_green.hole_y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance > 0:
                    dx /= distance
                    dy /= distance
                self.ball.position = (self.ball.position[0] + dx, self.ball.position[1] + dy)

        # Check if the ball lands in a hole
        if self.ball.on_green and self.ball.position == (self.ball.on_green.hole_x, self.ball.on_green.hole_y):
            for team in self.teams:
                if team.name == self.ball.on_green.team:
                    team.score += 1
                    break

        # Update the wind and obstacles
        self.physics_engine.wind.update()
        # TODO: Apply the effect of obstacles on the ball's trajectory

    def is_game_over(self):
        # Check if the game is over (e.g. after a certain number of turns or when a team reaches a certain score)
        return False  # TODO: Implement this method

    def output_game_state(self):
        # Output the current state of the game to a feed that can be displayed to the user
        # TODO: Implement this method
        pass