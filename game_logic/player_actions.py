import random

non_caddy_actions = ['block', 'drive', 'hit', 'idle', 'movement', 'pass_ball', 'precision_hit']

def choose_action(balls, players):
    action_determiner = random.randint(1, 100)
    for player in players:
        
        # Choose which ball to focus on
        ball = choose_ball(balls, players, player)
        # Determine the player's position and proximity to the ball
        position = player.position
        proximity = distance(player.position, ball.position)
        # Determine the possible actions for the player based on their position and proximity
        chosen_action = ''
        if player.position != 'caddy':
            if proximity < 1:
                if position == 'driver':
                    if action_determiner <= 40:
                        chosen_action= 'drive'
                    elif action_determiner <= 50:
                        chosen_action= 'precision_hit'
                    elif action_determiner <= 90:
                        chosen_action = 'hit'
                    else:
                        chosen_action = random.choice(non_caddy_actions)
                elif position == 'blocker':
                    if action_determiner <= 40:
                        chosen_action = 'block'
                    elif action_determiner <= 50:
                        chosen_action = 'hit'
                    elif action_determiner <= 90:
                        chosen_action = 'pass_ball'
                    else:
                        chosen_action = random.choice(non_caddy_actions)
                elif position == 'marksman':
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
                chosen_action = 'flee_ball''
            else:
                if action_determiner <= 90:
                    chosen_action = 'idle'
                elif action_determiner <= 92:
                    chosen_action = 'offer_bribe'
                else:
                    chosen_action = 'hit'
        
        # Call the chosen action function with the player and ball objects as arguments to ensure ball focus does not change
        if chosen_action:
            action_function = globals()[chosen_action]
            action_function(player, ball)

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

def distance(pos1, pos2):
    # Calculate the distance between two positions
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def block(player, ball):
    success_prob = (player.balance + player.power + player.solidity)
    if random.randint(0, 20) < success_prob:
        ball.position = player.position
        ball.speed = 0
        ball.direction = 0

# def dive(player):
#    success_prob = (player.speed + player.balance + player.solidity)
#    return random.random() < success_prob

def drive(player, ball):
    success_prob = player.competitiveness + player.visual_calculus - abs(ball.velocity[0]) - abs(ball.velocity[1])
    if random.randint(0, 7) < success_prob:
        ball.velocity[0] += (player.power + player.accuracy) * random.uniform(0.5, 1.5)
        ball.velocity[1] += (player.power + player.accuracy)* random.uniform(0.5, 1.5)
        ball.velocity[2] += player.power * random.uniform(0.5, 1.5)
    else:
        print('drive failed')

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