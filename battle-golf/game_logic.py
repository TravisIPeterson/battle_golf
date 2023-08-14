import numpy as np
from models.player import Player
from models.green import Green
from models.team import Team
import random

class GameLogic:
    def __init__(self):
        # Initialize two teams of players (for simplicity, each team has one of each role)
        self.team_A = [Player(role="driver"), Player(role="marksman"), Player(role="blocker"), Player(role="goalie")]
        self.team_B = [Player(role="driver"), Player(role="marksman"), Player(role="blocker"), Player(role="goalie")]
        self.ball_position = (0, 0)
        self.turns = 20  # Play for 20 turns for simplicity

    def play_turn(self, player):
        # Check if the player wants to go for the ball
        if player.should_go_for_ball(self.ball_position):
            # Decide the action based on the player's role
            if player.role == "driver":
                target_green = player.select_green()
                # Simulate the drive
                result_green = player.drive(target_green, player.green_number)
                if result_green:
                    self.ball_position = (result_green, 0)
                else:
                    # Ball does not land on any green
                    self.ball_position = (-1, -1)

            elif player.role == "marksman":
                chosen_green, aim_for_player = player.aimed_shot(list(range(1, 9)), self.team_A + self.team_B)
                if aim_for_player:
                    # The ball position remains the same, but a player is potentially hit
                    hit_player = next(p for p in (self.team_A + self.team_B) if p.green_number == chosen_green)
                    hit_player.green_number = 0  # The player is hit and sent to a penalty green
                else:
                    self.ball_position = (chosen_green, 0)

            elif player.role == "blocker":
                if player.block(self.ball_position):
                    # Successful block, ball's position remains the same but is with the blocker
                    self.ball_position = player.position

            elif player.role == "goalie":
                if not player.save(self.ball_position):
                    # Goalie failed to save, ball remains in its position and goalie may fall into a hole
                    if random.random() > player.calculate_save_probability(0, 0):  # Using dummy values for speed and direction for now
                        player.fall_into_hole()

            player.neoliberal_agenda(self.team_A + self.team_B)

    def play_game(self):
        for turn in range(self.turns):
            print(f"\nTurn {turn + 1}:")

            # Players from team A take their turns
            for player in self.team_A:
                self.play_turn(player)

            # Players from team B take their turns
            for player in self.team_B:
                self.play_turn(player)

            # At the end of each turn, you can calculate scores, display stats, or make other game-related decisions

        print("\nGame Over!")

# To play the game
game = GameLogic()
game.play_game()