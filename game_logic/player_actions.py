import random
import traceback
import math
from game_state import Coordinates
from entities.ball import Ball
from action_helpers import distance, choose_ball, choose_teammate_target
from blocker_actions import determine_blocker_action
from driver_actions import determine_driver_action

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
                        determine_driver_action(player, players, player.targeted_ball, greens, wind)
                    elif player.position == 'goalie':
                        determine_driver_action(player, players, player.targeted_ball, greens, wind)
                    elif player.position == 'caddy':
                        determine_driver_action(player, players, player.targeted_ball, greens, wind)

    except Exception as e:
        print(f"Error in choose_action: {e}")
        traceback.print_exc()

'''
CODE BEING BROKEN UP INTO POSITION-SPECIFIC FUNCTIONS

def determine_blocker_action(player, balls, greens, wind):        
def determine_player_action(player, proximity, greens, wind):
    action_determiner = random.uniform(0, 100)
    chosen_action = 'pursue_ball'
    proximity = distance(player.coordinates, player.targeted_ball.coordinates)
    if player.position != 'caddy':
        if proximity < 5 and player.targeted_ball.z < 10:
            if player.position: # == 'driver':
                if action_determiner <= 0:
                    chosen_action= 'drive'
                elif action_determiner <= 10000000:
                    chosen_action= 'precision_hit'
                elif action_determiner <= 90:
                    chosen_action = 'hit'
                else:
                    chosen_action = random.choice(non_caddy_actions)
            elif player.position == 'blocker':
                if action_determiner <= 40:
                    chosen_action = 'block'
                elif action_determiner <= 50:
                    chosen_action = 'hit'
                elif action_determiner <= 90:
                    chosen_action = 'pass_ball'
                else:
                    chosen_action = random.choice(non_caddy_actions)
            elif player.position == 'marksman':
                if action_determiner <= 70:
                    chosen_action = 'precision_hit'
                elif action_determiner <= 80:
                    chosen_action = 'hit'
                elif action_determiner <= 90:
                    chosen_action = 'pass_ball'
                else:
                    chosen_action = random.choice(non_caddy_actions)
            else:
                if action_determiner <= 95:
                    chosen_action = 'block'
                else:
                    chosen_action = random.choice(non_caddy_actions)
        else:
            chosen_action = 'pursue_ball'
    else:
        if proximity < 10:
            chosen_action = 'flee_ball'
        else:
            if action_determiner <= 90:
                chosen_action = 'idle'
            elif action_determiner <= 92:
                chosen_action = 'offer_bribe'
            else:
                chosen_action = 'hit'
    return chosen_action
'''

def block(player, players, ball, greens, wind):
    success_prob = (player.balance + player.power + player.solidity)
    if random.randint(0, 30) < success_prob:
        ball.x = player.x
        ball.y = player.y
        ball.velocity = [0, 0, 0]  # Reset all components of the velocity
        player.targeted_opponent = choose_teammate_target(player, players)
        player.action_in_progress = 'pass_ball'

# def dive(player):
#    success_prob = (player.speed + player.balance + player.solidity)
#    return random.random() < success_prob

def drive(player, players, ball, greens, wind):
    proximity = distance(player.coordinates, ball.coordinates)
    success_prob = player.competitiveness + player.visual_calculus - abs(ball.velocity[0]) - abs(ball.velocity[1])
    if proximity < 6:
        if random.randint(0, 7) < success_prob:
            direction_x, direction_y = player.aim(greens, wind)
            ball.velocity[0] += (direction_x * player.power) * random.uniform(0.1, 0.15)
            ball.velocity[1] += (direction_y * player.power) * random.uniform(0.1, 0.15)
            ball.velocity[2] += player.power * random.uniform(0.3, 0.7)
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

def idle(player):
    return True
'''

def mill_about(player, players, ball, greens, wind):
    # Define the range of random offsets (within 20 units from the edge of the green)
    offset_range = 20

    while True:
        # Randomly choose an angle
        angle = random.uniform(0, 2 * math.pi)

        # Calculate the random offset distance from the green's edge
        offset_distance = random.uniform(0, offset_range)
        green = next((green for green in greens if green.team == player.team_id), None)

        # Calculate the target coordinates
        target_x = green.x + (green.radius + offset_distance) * math.cos(angle)
        target_y = green.y + (green.radius + offset_distance) * math.sin(angle)
        coord = Coordinates(target_x, target_y, 0)

        # Check if the target is at least 50 units away from the player's current position
        if distance(player.coordinates, coord) >= 50:
            break

    player.move((target_x, target_y), greens, wind)

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
    player.action_in_progress = None
    player.targeted_ball = None
    return True

def precision_hit(player, players, ball, greens, wind):
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
        else:
            print(f"{player.name} had a change of heart.")
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
    if distance((player.coordinates), (ball.coordinates)) < 5:
        player.action_in_progress = None
        return True
    else:
        return False

# def resist_bribe(player):
    # success_prob = (player.integrity + player.cowardice) / 20.0
    # return random.random() < success_prob