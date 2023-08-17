import random

from models.players.player_base import Player
from models.players.actions.defensive_actions import DefensiveActions
from models.players.actions.miscellaneous_actions import MiscellaneousActions
from models.players.actions.offensive_actions import OffensiveActions
from models.green import Green
from models.team import Team

class GameLogic:
    def __init__(self):
        # Initialize 8 teams and distribute them across 8 greens
        self.teams = [Team(i+1) for i in range(8)]
        for i, team in enumerate(self.teams):
            team.players['Driver'].green_number = i + 1
            
        self.ball_green_number = 1  # Starting ball position on Green 1
        self.turns = 20  # Play for 20 turns for simplicity
        self.all_greens = list(range(1, 9))
        self.action_history = []

    def get_team_on_green(self, green_number):
        for team in self.teams:
            if team.players['Driver'].green_number == green_number:  # Using the Driver as a reference, assuming all team members are on the same green
                return team
        return None

    def play_turn(self, players):
        available_actions = self.determine_available_actions
        chosen_action = random.choice(available_actions)
        acting_player = self.select_player_for_action(chosen_action)
        getattr(acting_player, chosen_action)()
        self.action_history.append((acting_player, chosen_action))

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
