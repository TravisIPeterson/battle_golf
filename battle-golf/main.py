
from models import Team, Ball, Green, Player
from game_logic import BattleGolf

def main():
    # Initialize teams, ball, greens, etc.
    teams = [Team("TeamA"), Team("TeamB"), ...]
    ball = Ball()
    greens = [Green(i) for i in range(1, 9)]

    # Start game simulation
    game = BattleGolf(teams, ball, greens)
    game.play_game()

if __name__ == "__main__":
    main()