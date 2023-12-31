import random
import math
from game_state import Coordinates
from action_helpers import distance, find_blocker_green, is_player_near_green, move_toward_green, find_approaching_balls, intercept_ball

def determine_goalie_action(player, players, balls, greens, wind):
    goalie_green = find_blocker_green(player, greens)

    # Check if player is near green, if not, move toward green
    if not is_player_near_green(player, goalie_green, greens):
        move_toward_green(player, goalie_green, greens)
        return

    # Sort balls by proximity
    balls_sorted_by_proximity = find_approaching_balls(player, balls)

    # Select the nearest ball
    if distance(player.coordinates, balls_sorted_by_proximity[0].coordinates) > 50:
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


def adjust_path_for_goalie(player, green):
    # Calculate distance from the center of the green
    distance_from_center = distance(player.coordinates, Coordinates(green.x, green.y, 0))

    # If the goalie is too close to the center, adjust their path
    if distance_from_center < 5:
        # Calculate an angle from the center of the green to the player
        angle_to_player = math.atan2(player.y - green.y, player.x - green.x)

        # Set target coordinates just outside the 5-unit radius
        target_x = green.x + 5.1 * math.cos(angle_to_player)
        target_y = green.y + 5.1 * math.sin(angle_to_player)

        return Coordinates(target_x, target_y, 0)

    return player.target_coordinates

