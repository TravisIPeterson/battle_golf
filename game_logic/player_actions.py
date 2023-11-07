import random
import traceback
from entities.ball import Ball


non_caddy_actions = ['block', 'drive', 'hit', 'idle', 'movement', 'pass_ball', 'precision_hit']

def choose_action(balls, players):
    try:
        print("Entered choose_action")

        for ball in balls:
            if not hasattr(ball, 'last_acted_upon'):
                ball.last_acted_upon = 0

        for player in players:
            
            if player.action_in_progress:
                action_function = globals()[player.action_in_progress]
                action_completed = action_function(player, ball)
                if action_completed:
                    player.action_in_progress = None

            else:  
                action_determiner = random.randint(0, 100)        
                # Choose which ball to focus on
                ball = choose_ball(balls, players, player)
                # Update the last acted upon turn for the chosen ball
                ball.last_acted_upon = 0
                # For all other balls, increase the last acted upon counter
                for b in balls:
                    if b != ball:
                        b.last_acted_upon += 1

                proximity = distance(player.coordinates, ball.coordinates)
                # Determine the possible actions for the player based on their coords and proximity
                chosen_action = ''
                if player.position != 'caddy':
                    if proximity < 1:
                        if player.position == 'driver':
                            if action_determiner <= 40:
                                chosen_action= 'drive'
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

                player.action_in_progress = chosen_action
                # Call the chosen action function with the player and ball objects as arguments to ensure ball focus does not change

    except Exception as e:
        print(f"Error in choose_action: {e}")
        traceback.print_exc()

def choose_ball(balls, players, player):
    team_players = [p for p in players if p.team_id == player.team_id and p != player]
    opposing_players = [p for p in players if p.team_id != player.team_id]
    ball_scores = []
    for ball in balls:
        # Calculate the score for the ball based on the number of players near it
        team_score = sum([1 for p in team_players if distance(p.coordinates, ball.coordinates) < 10])
        opposing_score = sum([1 for p in opposing_players if distance(p.coordinates, p.coordinates) < 10])
        score = team_score * player.competitiveness / player.cowardice - opposing_score
        # Adjust score based on last acted upon value
        score += ball.last_acted_upon * 0.5  # This gives some preference to balls that haven't been acted upon recently
        ball_scores.append((ball, score))
    # Choose the ball with the highest score
    ball_scores.sort(key=lambda x: x[1], reverse=True)
    best_ball = ball_scores[0][0]
    # Randomly choose a different ball if there are other balls with the same score
    same_score_balls = [b for b, s in ball_scores if s == ball_scores[0][1]]
    if len(same_score_balls) > 1:
        best_ball = random.choice(same_score_balls)
    return best_ball

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

def drive(player, ball):
    success_prob = player.competitiveness + player.visual_calculus - abs(ball.velocity[0]) - abs(ball.velocity[1])
    if random.randint(0, 7) < success_prob:
        ball.velocity[0] += (player.power + player.accuracy) * random.uniform(0.5, 1.5)
        ball.velocity[1] += (player.power + player.accuracy) * random.uniform(0.5, 1.5)
        ball.velocity[2] += player.power * random.uniform(0.5, 1.5)
    else:
        print('drive failed')

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

def pursue_ball(player, ball):

    # Move the player towards the ball's x, y coordinates
    player.move((ball.x, ball.y))

    # After moving, check if the player is close enough to interact with the ball
    if distance((player.coordinates), (ball.coordinates)) < 1:
        return True
    else:
        return False

# def resist_bribe(player):
    # success_prob = (player.integrity + player.cowardice) / 20.0
    # return random.random() < success_prob