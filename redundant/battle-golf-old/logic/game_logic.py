import random

from models.players.player_base import Player
from models.players.actions.defensive_actions import DefensiveActions
from models.players.actions.miscellaneous_actions import MiscellaneousActions
from models.players.actions.offensive_actions import OffensiveActions
from models.team import Team
from .game_state import GameState

TOTAL_TEAMS = 8
TOTAL_TURNS = 20

class GameLogic:

    def __init__(self):
        self.initialize_game()
        self.game_state = GameState()

    def initialize_game(self):
        self.teams = [Team(i + 1) for i in range (TOTAL_TEAMS)]
        for i, team in enumerate(self.teams):
            team.players['Drivers'].green_number = i + 1

        self.ball_green_number = random.randint(1..8)
        self.turns = TOTAL_TURNS
        self.all_greens = list(range(1, TOTAL_TEAMS +1))

    def get_team_on_green(self, green_number):
        return self.team.green_number == green_number

    def play_turn(self, players):
        available_actions = self.game_state.available_actions
        chosen_action = random.choice(available_actions)
        acting_player = self.select_player_for_action(chosen_action)
        action_method = getattr(acting_player, chosen_action, None)

        if action_method and callable(action_method):
            action_method()
            self.game_state.perform_transition(chosen_action)
        else:
            print(f"Error: '{chosen_action}' is not a valid action for {acting_player}.")

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
