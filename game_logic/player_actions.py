import random
import traceback
import math
from game_state import Coordinates
from entities.ball import Ball
from entities.wall import Wall
from action_helpers import distance, choose_ball, choose_teammate_target, find_approaching_balls, find_nearby_opponent, is_bribed
from blocker_actions import determine_blocker_action
from driver_actions import determine_driver_action
from marksman_actions import determine_marksman_action
from goalie_actions import determine_goalie_action
from caddy_actions import determine_caddy_action

def choose_action(balls, players, greens, wind):
    try:
        # Increment last_acted_upon for all balls
        for ball in balls:
            ball.last_acted_upon += 1

        # Iterate over each player to determine their action
        for player in players:

            # If player has an action in progress, continue it
            if player.action_in_progress and not is_bribed(player):
                action_function = globals()[player.action_in_progress]
                if player.action_in_progress == "mill_about":
                    action_completed = action_function(player, players, balls, greens, wind)
                else:
                    action_completed = action_function(player, players, player.targeted_ball, greens, wind)

                if action_completed:
                    player.action_in_progress = None
                    player.targeted_ball = None
            else:
                # Choose a new ball if the player doesn't have one targeted
                if player.targeted_ball is None:
                    player.targeted_ball = choose_ball(balls, players, player, greens)
                
                if player.targeted_ball:
                    if player.position == 'driver':
                        determine_driver_action(player, players, player.targeted_ball, greens, wind)
                    elif player.position == 'blocker':
                        determine_blocker_action(player, players, balls, greens, wind)
                    elif player.position == 'marksman':
                        determine_marksman_action(player, players, player.targeted_ball, greens, wind)
                    elif player.position == 'goalie':
                        determine_goalie_action(player, players, balls, greens, wind)
                    elif player.position == 'caddy':
                        determine_caddy_action(player, players, balls, greens, wind)

    except Exception as e:
        print(f"Error in choose_action: {e}")
        traceback.print_exc()

def block(player, players, ball, greens, wind):
    if distance(player.coordinates, ball.coordinates) < 5:
        success_prob = (player.balance + player.power + player.solidity)
        if random.randint(0, 30) < success_prob and ball.last_hit_by != player:
            ball.x = player.x
            ball.y = player.y
            ball.velocity = [0, 0, 0]  # Reset all components of the velocity
            player.targeted_opponent = choose_teammate_target(player, players)
            player.action_in_progress = 'pass_ball'
        else:
            player.action_in_progress = None
            player.targeted_ball = None
            return True
    else:
        player.action_in_progress = None
        player.targeted_ball = None
        return True

def drive(player, players, ball, greens, wind):
    proximity = distance(player.coordinates, ball.coordinates)
    if proximity < 3 and ball.last_hit_by != player:
        if player.competitiveness + player.tenacity > abs(ball.velocity[0]) * abs(ball.velocity[1]):
            direction_x, direction_y = player.aim(greens, wind)
            ball.velocity[0] += (direction_x * player.power) * random.uniform(0.1, 0.15)
            ball.velocity[1] += (direction_y * player.power) * random.uniform(0.1, 0.15)
            ball.velocity[2] += player.power * random.uniform(0.3, 0.7)
            ball.last_hit_by = player
        else:
            print('drive failed')
            if player.tenacity > random.uniform(6, 10) and proximity < 6:  # Retry if tenacity is high and ball is still near
                print('retrying drive')
                return drive(player, players, ball, greens, wind)
    player.action_in_progress = None
    player.targeted_ball = None
    return True

def flee_ball(player, players, ball, greens, wind):
    # Determine direction opposite to ball
    direction_x = player.x - ball.x
    direction_y = player.y - ball.y

    # Move the player away from the ball's x, y coordinates
    player.move((direction_x, direction_y), greens, wind)

    # After moving, check if the player is far enough away from the ball to stop fleeing
    if distance((player.coordinates), (ball.coordinates)) > 10:
        player.action_in_progress = None
        return True
    else:
        return False

def mill_about(player, players, balls, greens, wind):
    # Check if the player already has a target to mill about
    if distance(player.coordinates, player.target_coordinates) < 5:
        while True:
            # Randomly choose an angle
            angle = random.uniform(0, 2 * math.pi)

            # Find the player's green
            green = next((g for g in greens if g.team == player.team_id), None)

            if player.position == 'goalie':
                # Goalies mill about within 5 to 30 units from the green's center
                offset_distance = random.uniform(5, 30)
                minimum_distance = 20
                # Calculate the target coordinates
                target_x = green.x + offset_distance * math.cos(angle)
                target_y = green.y + offset_distance * math.sin(angle)
            elif player.position == 'blocker':
                # Blockers can mill about within a larger range
                offset_distance = random.uniform(0, green.radius + 20)
                minimum_distance = 50
                # Calculate the target coordinates
                target_x = green.x + offset_distance * math.cos(angle)
                target_y = green.y + offset_distance * math.sin(angle)
            else:
                # Other players mill about anywhere within the wall
                wall = Wall(greens)
                offset_distance = random.uniform(0, wall.radius)  # Distance within the wall's radius
                minimum_distance = 50  # Minimum distance for target change, adjust as needed

                # Calculate the target coordinates within the wall
                target_x = wall.x + offset_distance * math.cos(angle)
                target_y = wall.y + offset_distance * math.sin(angle)
            
            coord = Coordinates(target_x, target_y, 0)

            # Check if the target is at least minimum_distance units away from the player's current position
            if distance(player.coordinates, coord) >= minimum_distance:
                player.target_coordinates = coord
                break

    stay_vigilant = find_approaching_balls(player, balls)
    if stay_vigilant and distance(player.coordinates, stay_vigilant[0].coordinates) < (player.twitchiness * 10):
        player.action_in_progress = None
        return True
                
    # Move the player toward the target position
    player.move(player.target_coordinates, greens, wind)

    if distance(player.coordinates, player.target_coordinates) < 5:
        player.action_in_progress = None
        player.target_coordinates = player.coordinates
        return True

def offer_bribe(player, players, ball, greens, wind):
    player.targeted_opponent = find_nearby_opponent(player, players)
    if player.targeted_opponent.throwing_the_game == True:
        player.action_in_progress = 'mill_about'
        player.targeted_opponent = None
        return True
    if distance(player.coordinates, player.targeted_opponent.coordinates) > 3:
        player.move(player.targeted_opponent.coordinates, greens, wind)
    else:
        if (player.neoliberalism + player.charisma) * random.random() > (player.targeted_opponent.integrity + player.targeted_opponent.greed) * random.random():
            player.targeted_opponent.throwing_the_game = True
            player.targeted_opponent.personal_clock = player.charisma * player.targeted_opponent.cowardice * player.targeted_opponent.greed * player.targeted_opponent.neoliberalism
            print(f"{player.name} bribed {player.targeted_opponent.name} to throw the game!")
        else:
            print(f"{player.name} tried to bribe {player.targeted_opponent.name} but failed!")
    player.action_in_progress = None
    player.targeted_opponent = None
    return True

def pass_ball(player, players, ball, greens, wind):
    direction_x, direction_y = player.aim_at_opponent(player.targeted_opponent)
    ball.velocity[0] += (direction_x * player.power) * random.uniform(0.1, 0.15)
    ball.velocity[1] += (direction_y * player.power) * random.uniform(0.1, 0.15)
    ball.velocity[2] += player.power * random.uniform(0.3, 0.7)
    player.targeted_opponent.targeted_ball = ball
    print("player passed ball")
    player.action_in_progress = None
    player.targeted_ball = None
    ball.last_hit_by = player
    return True

def precision_hit(player, players, ball, greens, wind):
    if ball.last_hit_by != player:
        proximity = distance(player.coordinates, ball.coordinates)
        if player.position == 'marksman':
            success_prob = player.dramatic_flair + player.savagery + player.accuracy - player.integrity - abs(ball.velocity[0]) - abs(ball.velocity[1])
        elif player.position == 'driver':
            success_prob = (player.dramatic_flair + player.savagery + player.accuracy - player.integrity - abs(ball.velocity[0]) - abs(ball.velocity[1])) * 0.5
        else:
            success_prob = 110
        if proximity < 6:
            if random.randint(0, 1) < success_prob:
                direction_x, direction_y = player.aim_at_opponent(player.targeted_opponent)
                ball.velocity[0] += (direction_x * player.power) * random.uniform(0.1, 0.15)
                ball.velocity[1] += (direction_y * player.power) * random.uniform(0.1, 0.15)
                ball.velocity[2] += player.power * random.uniform(0.3, 0.7)
                ball.last_hit_by = player
                print(f"{player.name} tries to knocks a precision strike toward {player.targeted_opponent.name}!")
            else:
                print(f"{player.name} had a change of heart.")
        player.action_in_progress = None
        player.targeted_ball = None
        player.targeted_opponent = None
        ball.last_hit_by = player
        return True
    else:
        player.action_in_progress = None
        player.targeted_ball = None
        player.targeted_opponent = None
        return True

def pursue_ball(player, players, ball, greens, wind):
    # If ball coordinates are off screen, action in progress is set to none
    if ball.coordinates.x < 0 or ball.coordinates.x > 1920 or ball.coordinates.y < 0 or ball.coordinates.y > 1080:
        player.action_in_progress = None
        player.targeted_ball = None
        return True
    
    prediction_frames = player.get_prediction_frames(ball)
    predicted_x, predicted_y, predicted_z = ball.predict_future_position(prediction_frames)

    # Move the player towards the ball's x, y coordinates
    player.move((predicted_x, predicted_y), greens, wind)

    # After moving, check if the player is close enough to interact with the ball
    if distance((player.coordinates), (ball.coordinates)) < 1:
        player.action_in_progress = None
        return True
    else:
        return False