import random
from action_helpers import distance

def determine_caddy_action(player, players, balls, greens, wind):
    danger_balls = []
    for ball in balls:
        if distance(player.coordinates, ball.coordinates) < 50:
            danger_balls.append(ball)
    if danger_balls:
        player.action_in_progress = 'flee_ball'
    else:
        action_determiner = random.uniform(0, 100)
        if action_determiner <= 99:
            player.action_in_progress = 'mill_about'
        elif action_determiner <= 100:
            player.action_in_progress = 'offer_bribe'
        elif action_determiner <= 75:
            player.action_in_progress = 'praise_teammate'
        elif action_determiner <= 100:
            player.action_in_progress = 'distract'