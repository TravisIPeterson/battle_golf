import random
import traceback
import math
from game_state import Coordinates
from entities.ball import Ball
from action_helpers import distance, choose_ball, choose_teammate_target
from blocker_actions import determine_blocker_action
from driver_actions import determine_driver_action
from marksman_actions import determine_marksman_action

non_caddy_actions = ['block', 'drive', 'hit', 'idle', 'movement', 'pass_ball', 'precision_hit']

def choose_action(balls, players, greens, wind):
    try:
        # Increment last_acted_upon for all balls
        for ball in balls:
            ball.last_acted_upon += 1

        # Iterate over each player to determine their action
        for player in players:

            # If player has an action in progress, continue it
            if player.action_in_progress:
                action_function = globals()[player.action_in_progress]
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
                        determine_driver_action(player, players, player.targeted_ball, greens, wind)
                    elif player.position == 'caddy':
                        determine_driver_action(player, players, player.targeted_ball, greens, wind)

    except Exception as e:
        print(f"Error in choose_action: {e}")
        traceback.print_exc()

def block(player, players, ball, greens, wind):
    if distance(player.coordinates, ball.coordinates) < 1:
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

# def dive(player):
#    success_prob = (player.speed + player.balance + player.solidity)
#    return random.random() < success_prob

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

'''
def hit(player):
    success_prob = (player.power + player.savagery) / 20.0
    return random.random() < success_prob
'''

def mill_about(player, players, ball, greens, wind):
    # Check if the player already has a target to mill about
    if distance(player.coordinates, player.target_coordinates) < 5:
        # Define the range of random offsets (within 20 units from the edge of the green)
        offset_range = 20

        while True:
            # Randomly choose an angle
            angle = random.uniform(0, 2 * math.pi)

            # Find the player's green
            green = next((green for green in greens if green.team == player.team_id), None)

            # Calculate the random offset distance from the green's edge
            offset_distance = random.uniform(0, offset_range)

            # Calculate the target coordinates
            target_x = green.x + (green.radius + offset_distance) * math.cos(angle)
            target_y = green.y + (green.radius + offset_distance) * math.sin(angle)
            coord = Coordinates(target_x, target_y, 0)

            # Check if the target is at least 50 units away from the player's current position
            if distance(player.coordinates, coord) >= 50:
                player.target_coordinates = coord
                break
                
    # Move the player toward the target position
    player.move(player.target_coordinates, greens, wind)

    if distance(player.coordinates, player.target_coordinates) < 5:
        player.action_in_progress = None
        player.target_coordinates = player.coordinates
        return True

'''
def movement(player):
    success_prob = (player.speed + player.balance) / 20.0
    return random.ran
        print(player.coordinates)
'''

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

# def resist_bribe(player):
    # success_prob = (player.integrity + player.cowardice) / 20.0
    # return random.random() < success_prob