import random
from action_helpers import find_blocker_green, is_player_near_green, move_toward_green, find_approaching_balls, intercept_ball

def determine_blocker_action(player, balls, greens, wind):
    blocker_green = find_blocker_green(player, greens)

    if not is_player_near_green(player, blocker_green, greens):
        move_toward_green(player, blocker_green, greens)
        return
    
    approaching_balls = find_approaching_balls(player, balls, blocker_green)
    if approaching_balls:
        if player.dramatic_flair > 7:
            if len(approaching_balls) > 1:
                player.targeted_ball = random.choice(approaching_balls)
        else:
            player.targeted_ball = approaching_balls[0]
        
        intercept_status = intercept_ball(player, player.targeted_ball, greens, wind)

        if intercept_status == "reached":
            player.action_in_progress = "block"
        elif intercept_status == "unreachable":
            player.action_in_progress = False