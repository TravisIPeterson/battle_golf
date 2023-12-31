import random
from action_helpers import distance, find_blocker_green, is_player_near_green, move_toward_green, find_approaching_balls, intercept_ball

def determine_blocker_action(player, players, balls, greens, wind):
    blocker_green = find_blocker_green(player, greens)

    # Check if player is near green, if not, move toward green
    if not is_player_near_green(player, blocker_green, greens):
        move_toward_green(player, blocker_green, greens)
        return

    # Sort balls by proximity
    balls_sorted_by_proximity = find_approaching_balls(player, balls)

    # Select the nearest ball
    if distance(player.coordinates, balls_sorted_by_proximity[0].coordinates) > 100:
        player.action_in_progress = "mill_about"
    else:
        player.targeted_ball = balls_sorted_by_proximity[0]
        intercept_status = intercept_ball(player, players, player.targeted_ball, greens, wind)

        # Update action based on intercept status
        if intercept_status == "reached":
            player.action_in_progress = "block"
        elif intercept_status == "ongoing":
            if player.tenacity - (player.twitchiness * random.random()) > random.uniform(5, 10):
                player.action_in_progress = "mill_about"
            else: 
                balls_sorted_by_proximity = find_approaching_balls(player, balls)
                if balls_sorted_by_proximity:
                    player.targeted_ball = balls_sorted_by_proximity[0]
                    intercept_ball(player, players, player.targeted_ball, greens, wind)
        else:
            player.action_in_progress = None
