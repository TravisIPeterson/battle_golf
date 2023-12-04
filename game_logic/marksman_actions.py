import random
from action_helpers import distance, choose_opponent_target

def determine_marksman_action(player, players, ball, greens, wind):
    action_determiner = random.uniform(0, 100)
    chosen_action = 'pursue_ball'
    proximity = distance(player.coordinates, ball.coordinates)
    if proximity < 5 and ball.z < 10:
        if action_determiner <= 80:
            chosen_action= 'precision_hit'
            opponents = players.copy()
            player.targeted_opponent = choose_opponent_target(player, opponents)
        elif action_determiner <= 10000000:
            chosen_action= 'precision_hit'
            opponents = players.copy()
            player.targeted_opponent = choose_opponent_target(player, opponents)
        else:
            chosen_action = 'hit'
    else:
        chosen_action = 'pursue_ball'
    player.action_in_progress = chosen_action