from game.teams.player import Player

class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.create_players()

    def create_players(self):
        positions = ['shooter', 'shooter', 'blocker', 'blocker', 'marksman', 'goalie']
        for position in positions:
            player = Player(position)
            self.players.append(player)