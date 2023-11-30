import random

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
        # Only consider balls that have coordinates which appear on screen
        if ball.coordinates.x > 0 and ball.coordinates.x < 1920 and ball.coordinates.y > 0 and ball.coordinates.y < 1080:
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

def choose_opponent_target(player, players):
    # Choose a player from an opposing team to target
    opposing_players = [p for p in players if p.team_id != player.team_id]
    # Cycle through all opponents and multiply charisma by a random number between 1 and 10; lowest charisma becomes target
    for p in opposing_players:
        p.target_score = p.charisma * random.randint(1, 10)
    opposing_players.sort(key=lambda x: x.target_score)
    return opposing_players[0] 

def distance(coord1, coord2):
    # Calculate the 2D distance between two positions using the Coordinates objects directly
    return ((coord1.x - coord2.x) ** 2 + (coord1.y - coord2.y) ** 2) ** 0.5

def find_approaching_balls(player, balls, green):
    approaching_balls = []
    intelligence_factor = player.intelligence / random.uniform(5, 10)
    visual_calculus_factor = player.visual_calculus / random.uniform(5, 10)
    precognition = (intelligence_factor + visual_calculus_factor)

    for ball in balls:
        future_x = ball.coordinates.x + ball.velocity[0] * precognition
        future_y = ball.coordinates.y + ball.velocity[1] * precognition
        future_z = ball.coordinates.z + ball.velocity[2] * precognition

        offset_range = [20, -20]

        if any(green.contains(future_x + dx, future_y + dy) and future_z < 20 for dx in offset_range for dy in offset_range):
            approaching_balls.append(ball)

    approaching_balls.sort(key=lambda b: distance(player.coordinates, b.coordinates))
    return approaching_balls

def find_blocker_green(player, greens):
    return next((green for green in greens if green.team == player.team_id), None)

def intercept_ball(player, ball, greens, wind):
    if ball.coordinates.z > 20:
        return "unreachable"
    # Base factors from player attributes
    intelligence_factor = player.intelligence / 100
    visual_calculus_factor = player.visual_calculus / 100
    cowardice_factor = player.cowardice / 100

    # Adjust the prediction and movement based on player attributes
    prediction_adjustment = random.uniform(-0.5, 0.5) * (1 - intelligence_factor + visual_calculus_factor)
    movement_adjustment = random.uniform(-0.5, 0.5) * (1 - cowardice_factor)

    # Player's speed (scalar)
    player_speed = player.speed  

    # Ball's speed (magnitude of its velocity vector)
    ball_speed = (ball.velocity[0]**2 + ball.velocity[1]**2 + ball.velocity[2]**2)**0.5

    # Calculate the 2D distance between the player and the ball
    distance_to_ball = distance(player.coordinates, ball.coordinates)

    # Calculate the time it will take the player to reach the current ball position
    time_to_reach_ball = distance_to_ball / player_speed

    # Predict the ball's future position with some randomness based on player's attributes
    future_x = ball.coordinates.x + ball.velocity[0] * ball_speed * time_to_reach_ball * (1 + prediction_adjustment)
    future_y = ball.coordinates.y + ball.velocity[1] * ball_speed * time_to_reach_ball * (1 + prediction_adjustment)

    # Calculate the direction from the player to the ball's future position
    direction_x = future_x - player.coordinates.x
    direction_y = future_y - player.coordinates.y
    distance_to_future = (direction_x**2 + direction_y**2)**0.5

    if distance_to_future > 0:
        direction_x /= distance_to_future
        direction_y /= distance_to_future

    # Calculate the target position with a movement adjustment
    target_x = player.coordinates.x + direction_x * player_speed * time_to_reach_ball * (1 + movement_adjustment)
    target_y = player.coordinates.y + direction_y * player_speed * time_to_reach_ball * (1 + movement_adjustment)

    # Move the player toward the adjusted target position
    player.move((target_x, target_y), greens, wind)

    # Return True if the player is close enough to the ball to interact with it
    if distance(player.coordinates, ball.coordinates) < 5:
        return "reached"
    else:
        return "ongoing"

def is_player_near_green(player, green, greens):
    offset_range = [20, -20]

    return any(green.contains(player.x + dx, player.y + dy) for dx in offset_range for dy in offset_range)

def move_toward_green(player, green, greens):
    direction_x = player.coordinates.x - green.x
    direction_y = player.coordinates.y - green.y
    distance_from_center = (direction_x ** 2 + direction_y ** 2) ** 0.5

    if distance_from_center > 0:
        direction_x /= distance_from_center
        direction_y /= distance_from_center

    target_x = green.x + direction_x * (green.radius + 20)
    target_y = green.y + direction_y * (green.radius + 20)

    player.move((target_x, target_y), greens, greens) #Wind not needed for function so passing greens an additional time to avoid error because I'm lazy