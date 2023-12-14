import random
import json
import time

class Coordinates:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def update(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        return iter((self.x, self.y, self.z))

class ActionLogManager:
    def __init__(self, comments_file):
        with open(comments_file, 'r') as file:
            self.comments = json.load(file)
        self.logs = []

    def add_log(self, action_type, player):
        if action_type in self.comments:
            comment_template = random.choice(self.comments[action_type])
            opponent_name = player.targeted_opponent.name if player.targeted_opponent else 'Blankenship'
            comment = comment_template.format(player=player.name, opponent=opponent_name)
            print("Comment template", comment_template)
            print("Player name", player)
            print("Opponent name", opponent_name)
            self.logs.append({'comment': comment, 'timestamp': time.time()})

    def get_active_logs(self):
        current_time = time.time()
        active_logs = []
        for log in self.logs:
            if current_time - log['timestamp'] < 10:
                active_logs.append(log['comment'])
            else:
                self.logs.remove(log)
        return active_logs