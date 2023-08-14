import numpy as np
from models.player import Player
from models.green import Green
from models.team import Team
import random

class GameLogic:
    def __init__(self):
        # Initialize 8 teams and distribute them across 8 greens
        self.teams = [Team(i+1) for i in range(8)]
        for i, team in enumerate(self.teams):
            team.players['Driver'].green_number = i + 1
            
        self.ball_green_number = 1  # Starting ball position on Green 1
        self.turns = 20  # Play for 20 turns for simplicity
        self.all_greens = list(range(1, 9))

    def get_team_on_green(self, green_number):
        for team in self.teams:
            if team.players['Driver'].green_number == green_number:  # Using the Driver as a reference, assuming all team members are on the same green
                return team
        return None

    def play_turn(self, player, ball_pursuers):
        print(f"{player.role} is starting their turn.")
        # Check if the player wants to go for the ball
        pursuing = player.should_go_for_ball(self.ball_green_number, len(ball_pursuers))
        if pursuing:
            ball_pursuers.append(player)

            if player.role == "blocker":
                if player.block(self.ball_green_number):
                    # Successful block, ball's position remains the same but is with the blocker
                    print(f"{player.role} from Team {player.team_name} blocked the ball. Ball is now on Green {self.ball_green_number}")  # Debugging line
            
            elif player.role == "marksman":
                all_players = [p for team in self.teams for p in team.players.values()]
                chosen_green, aim_for_player = player.aimed_shot(list(range(1, 9)), all_players)
                if aim_for_player:
                    assert all(p.green_number != 0 for p in all_players)
                    hit_player = next(p for p in all_players if p.green_number == chosen_green)
                else:
                    self.ball_green_number = chosen_green

            elif player.role == "goalie":
                if not player.save():
                    if random.random() > player.calculate_save_probability(0, 0):
                        player.fall_into_hole()

            all_players = [player for team in self.teams for player in team.players.values()]
            player.neoliberal_agenda(all_players)

    def play_game(self):
        for turn in range(self.turns):
            print(f"\nTurn {turn + 1}:")
            print(f"Ball is currently on Green {self.ball_green_number}")  # Debugging line

            current_team = self.get_team_on_green(self.ball_green_number)
            if not current_team:
                print("Error: No team found on current green!")
                break
            
            ball_pursuers = []  # Reset list of players pursuing the ball for this turn

            # Players from team A and B take their turns
            for player in current_team.players.values():
                self.play_turn(player, ball_pursuers)  
            
            # Determine which player actually gets the ball based on player's calculated speed
            if ball_pursuers:  # Check if there are any pursuers
                # Use the calculate_speed() function for each player to get their current speed
                fastest_player = max(ball_pursuers, key=lambda player: player.calculate_speed())
                
                # The fastest player gets the ball
                self.ball_green_number = fastest_player.green_number
                
                # Print the result
                random_msg = random.choice([
                    f"{fastest_player.role.capitalize()} from {fastest_player.team_name} reached the ball first!",
                    f"{fastest_player.role.capitalize()} from {fastest_player.team_name} was the quickest to the ball!",
                    f"Speedy {fastest_player.role} from {fastest_player.team_name} grabbed the ball!"
                ])
                print(random_msg)

            # At the end of each turn, you can calculate scores, display stats, or make other game-related decisions

        print("\nGame Over!")

# To play the game
game = GameLogic()
game.play_game()
