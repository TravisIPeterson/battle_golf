import game_logic
from models.player import Player
from  models.green import Green
import numpy as np

def test_players_react_to_ball_approaching_green():
    # Set up the game

    driver = Player('driver', {'Speed': 15, 'Competitiveness': 12, 'Visual Calculus': 4, 'Balance': 16, 
                'Solidity': 12, 'Savagery': 20, 'Cowardice': 17, 'Neoliberalism': 2,
                'Integrity': 4})
    marksman = Player('marksman', {'Speed': 1, 'Competitiveness': 8, 'Visual Calculus': 3, 'Balance': 17, 
                'Solidity': 11, 'Savagery': 12, 'Cowardice': 7, 'Neoliberalism': 19,
                'Integrity': 5})
    blocker = Player('blocker', {'Speed': 8, 'Competitiveness': 8, 'Visual Calculus': 8, 'Balance': 8, 
                'Solidity': 20, 'Savagery': 8, 'Cowardice': 8, 'Neoliberalism': 8,
                'Integrity': 8})
    goalie = Player('goalie', {'Speed': 12, 'Competitiveness': 6, 'Visual Calculus': 4, 'Balance': 15, 
                'Solidity': 13, 'Savagery': 3, 'Cowardice': 9, 'Neoliberalism': 12,
                'Integrity': 10})
    dummy_players = [
    Player("driver", {'Speed': 15, 'Competitiveness': 12, 'Visual Calculus': 4, 'Balance': 16, 
                'Solidity': 12, 'Savagery': 20, 'Cowardice': 17, 'Neoliberalism': 2,
                'Integrity': 4}),
    Player("marksman", {'Speed': 1, 'Competitiveness': 8, 'Visual Calculus': 3, 'Balance': 17, 
                'Solidity': 11, 'Savagery': 12, 'Cowardice': 7, 'Neoliberalism': 19,
                'Integrity': 5}),
    Player("blocker", {'Speed': 8, 'Competitiveness': 8, 'Visual Calculus': 8, 'Balance': 8, 
                'Solidity': 20, 'Savagery': 8, 'Cowardice': 8, 'Neoliberalism': 8,
                'Integrity': 8}),
    Player("goalie", {'Speed': 12, 'Competitiveness': 6, 'Visual Calculus': 4, 'Balance': 15, 
                'Solidity': 13, 'Savagery': 3, 'Cowardice': 9, 'Neoliberalism': 12,
                'Integrity': 10})
    # ... add more players as necessary
    ]

    dummy_players = [driver, marksman, blocker, goalie]

    dummy_greens = [
        Green(number=1),
        Green(number=2),
        Green(number=3),
        Green(number=4),
        Green(number=5),
        Green(number=6),
        Green(number=7),
        Green(number=8),
        # ... add more greens as necessary
    ]

    game = game_logic.GameLogic(dummy_players, dummy_greens)

    # Simulate ball approaching the green
    game.ball_approaching_green()

    # Check if players reacted as expected
    assert driver.should_go_for_ball(game.ball_position) == True, "Driver did not react to ball approaching green."
    assert marksman.should_go_for_ball(game.ball_position) == True, "Marksman did not react to ball approaching green."

    print("Test passed!")

test_players_react_to_ball_approaching_green()
