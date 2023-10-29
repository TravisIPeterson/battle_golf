import random

def get_possible_actions(balls, players):
    actions = {}
    for player in players:
        
        # Choose which ball to focus on
        ball = choose_ball(balls, players, player)
        # Determine the player's position and proximity to the ball
        position = player.position
        proximity = distance(player.position, ball.position)
        # Determine the possible actions for the player based on their position and proximity
        possible_actions = []
        if player.position != 'caddy':
            if proximity < 1:
                if position == 'driver':
                    possible_actions.append('drive')
                    possible_actions.append('precision_hit')
                    possible_actions.append('pass_ball')
                elif position == 'blocker':
                    possible_actions.append('block')
                    possible_actions.append('hit')
                    possible_actions.append('pass_ball')
                elif position == 'marksman':
                    possible_actions.append('precision_hit')
                    possible_actions.append('pass_ball')
                else:
                    possible_actions.append('pass_ball')
            else:
                possible_actions.append('pursue_ball')
                possible_actions.append('hit')
            actions[player] = possible_actions
        else:
            actions[player] = ['idle']
    return actions

def choose_ball(balls, players, player):
    # Determine which ball the player should focus on
    team_players = [p for p in players if p.team == player.team and p != player]
    opposing_players = [p for p in players if p.team != player.team]
    ball_scores = []
    for ball in balls:
        # Calculate the score for the ball based on the number of players near it
        team_score = sum([1 for p in team_players if distance(p.position, ball.position) < 10])
        opposing_score = sum([1 for p in opposing_players if distance(p.position, ball.position) < 10])
        score = team_score * player.competitiveness / player.cowardice - opposing_score
        ball_scores.append((ball, score))
    # Choose the ball with the highest score
    ball_scores.sort(key=lambda x: x[1], reverse=True)
    best_ball = ball_scores[0][0]
    # Randomly choose a different ball if there are other balls with the same score
    same_score_balls = [b for b, s in ball_scores if s == ball_scores[0][1]]
    if len(same_score_balls) > 1:
        best_ball = random.choice(same_score_balls)
    return best_ball

def block(player):
    if player.position == 'blocker':
        success_prob = (player.balance + player.power + player.solidity) / 30.0
    else:
        success_prob = (player.balance + player.power + player.solidity) / 60.0
    return random.random() < success_prob

def dive(player):
    success_prob = (player.speed + player.balance + player.solidity) / 30.0
    return random.random() < success_prob

def distance(pos1, pos2):
    # Calculate the distance between two positions
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def drive(player):
    if player.position == 'driver':
        success_prob = (player.power + player.accuracy) / 20.0
    else:
        success_prob = (player.power + player.accuracy) / 40.0
    return random.random() < success_prob

def hit(player):
    success_prob = (player.power + player.savagery) / 20.0
    return random.random() < success_prob

def idle(player):
    return True

def movement(player):
    success_prob = (player.speed + player.balance) / 20.0
    return random.random() < success_prob

def offer_bribe(player):
    success_prob = (player.greed + player.integrity) / 20.0
    return random.random() < success_prob

def pass_ball(player):
    success_prob = (player.accuracy + player.charisma) / 20.0
    return random.random() < success_prob

def precision_hit(player):
    if player.position == 'marksman':
        success_prob = (player.accuracy + player.competitiveness + player.dramatic_flair) / 30.0
    else:
        success_prob = (player.accuracy + player.competitiveness + player.dramatic_flair) / 60.0
    return random.random() < success_prob

def pursue_ball(player):
    success_prob = (player.speed + player.balance) / 20.0
    return random.random() < success_prob

def resist_bribe(player):
    success_prob = (player.integrity + player.cowardice) / 20.0
    return random.random() < success_prob