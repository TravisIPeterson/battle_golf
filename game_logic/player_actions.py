import random
import traceback
from entities.ball import Ball

non_caddy_actions = ['block', 'drive', 'hit', 'idle', 'movement', 'pass_ball', 'precision_hit']

def choose_action(balls, players, greens, wind):
    try:
        # Increment last_acted_upon for all balls
        for ball in balls:
            ball.last_acted_upon += 1

        # Iterate over each player to determine their action
        for player in players:
            if player.name == 'Pimento Wolf':
                print(player.targeted_ball)
                print(player.action_in_progress)
                print(player.action_completed)
            # If player has an action in progress, continue it
            if player.action_in_progress:
                action_function = globals()[player.action_in_progress]
                action_completed = action_function(player, player.targeted_ball, greens, wind)
                if action_completed:
                    player.action_in_progress = None
                    player.targeted_ball = None
            else:
                # Choose a new ball if the player doesn't have one targeted
                if player.targeted_ball is None:
                    player.targeted_ball = choose_ball(balls, players, player, greens)

                # Reset the last acted upon turn for the chosen ball
                if player.targeted_ball:
                    player.targeted_ball.last_acted_upon = 0
                    # For all other balls, increase the last acted upon counter
                    for b in balls:
                        if b != player.targeted_ball:
                            b.last_acted_upon += 1

                # Determine the player's action
                if player.targeted_ball:  # Ensure there is a targeted ball
                    proximity = distance(player.coordinates, player.targeted_ball.coordinates)
                    chosen_action = determine_player_action(player, proximity, greens, wind)
                    player.action_in_progress = chosen_action

    except Exception as e:
        print(f"Error in choose_action: {e}")
        traceback.print_exc()
        
def determine_player_action(player, proximity, greens, wind):
    action_determiner = random.uniform(0, 100)
    chosen_action = 'pursue_ball'
    proximity = distance(player.coordinates, player.targeted_ball.coordinates)
    if player.position != 'caddy':
        if proximity < 5 and player.targeted_ball.z < 10:
            if player.position: # == 'driver':
                if action_determiner <= 1000000:
                    chosen_action= 'drive'
                '''
                elif action_determiner <= 50:
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
            '''
        else:
            chosen_action = 'pursue_ball'
    '''
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
    '''
    return chosen_action

def choose_ball(balls, players, player, greens):
    # Track how many players are targeting each ball
    ball_target_count = {ball: 0 for ball in balls}
    for p in players:
        if p.targeted_ball:
            ball_target_count[p.targeted_ball] += 1

    # Maximum number of players that can target the same ball
    max_targets_per_ball = len(players) // len(balls)

    # Calculate scores for each ball, taking into account the proximity and other factors.
    ball_scores = []
    for ball in balls:
        # Skip balls that are at maximum targeting capacity or on another team's green
        if ball_target_count[ball] >= max_targets_per_ball:
            continue
        for green in greens:
            if green.team != player.team_id and green.contains(ball.coordinates.x, ball.coordinates.y):
                continue

        # Other scoring remains the same
        team_score = sum(1 for p in players if p.team_id == player.team_id and p != player and distance(p.coordinates, ball.coordinates) < 10)
        opposing_score = sum(1 for p in players if p.team_id != player.team_id and distance(p.coordinates, ball.coordinates) < 10)
        score = (team_score * player.competitiveness / (player.cowardice + 0.1)) - opposing_score
        score += 10 * ball.last_acted_upon

        # Adjust score based on how many players are already targeting this ball
        score /= (1 + ball_target_count[ball])

        ball_scores.append((ball, score))

    # Check if the total sum of scores is greater than zero
    total_score = sum(score for ball, score in ball_scores)
    if total_score <= 0:
        # If total score is not greater than zero, select a ball randomly
        return random.choice(balls)

    # Sort the balls by their score
    ball_scores.sort(key=lambda x: x[1], reverse=True)

    # Check if the highest score is negative, and if so, choose a ball randomly
    if ball_scores[0][1] < 0:
        return random.choice(balls)

    # Otherwise, return the ball with the highest score
    return ball_scores[0][0]

def distance(coord1, coord2):
    # Calculate the 2D distance between two positions using the Coordinates objects directly
    return ((coord1.x - coord2.x) ** 2 + (coord1.y - coord2.y) ** 2) ** 0.5

def block(player, ball):
    success_prob = (player.balance + player.power + player.solidity)
    if random.randint(0, 20) < success_prob:
        ball.x = player.x
        ball.y = player.y
        ball.velocity = [0, 0, 0]  # Reset all components of the velocity

# def dive(player):
#    success_prob = (player.speed + player.balance + player.solidity)
#    return random.random() < success_prob

def drive(player, ball, greens, wind):
    proximity = distance(player.coordinates, ball.coordinates)
    success_prob = player.competitiveness + player.visual_calculus - abs(ball.velocity[0]) - abs(ball.velocity[1])
    if proximity < 6:
        if random.randint(0, 7) < success_prob:
            direction_x, direction_y = player.aim(greens, wind)
            ball.velocity[0] += (direction_x * player.power) * 0.07
            ball.velocity[1] += (direction_y * player.power) * 0.07
            ball.velocity[2] += player.power * random.uniform(0.3, 0.7)
        else:
            print('drive failed')
            if player.tenacity > random.uniform(6, 10) and proximity < 6:  # Retry if tenacity is high and ball is still near
                print('retrying drive')
                return drive(player, ball, greens, wind)
    player.action_in_progress = None
    player.targeted_ball = None
    return True

'''
def hit(player):
    success_prob = (player.power + player.savagery) / 20.0
    return random.random() < success_prob

def idle(player):
    return True

def movement(player):
    success_prob = (player.speed + player.balance) / 20.0
    return random.ran
        print(player.coordinates)
def pass_ball(player):
    success_prob = (player.accuracy + player.charisma) / 20.0
    return random.random() < success_prob

def precision_hit(player):
    if player.position == 'marksman':
        success_prob = (player.accuracy + player.competitiveness + player.dramatic_flair) / 30.0
    else:
        success_prob = (player.accuracy + player.competitiveness + player.dramatic_flair) / 60.0
    return random.random() < success_prob
'''

def pursue_ball(player, ball, greens, wind):
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