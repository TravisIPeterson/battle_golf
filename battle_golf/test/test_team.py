import unittest
from game.teams.player import Player
from game.teams.team import Team

class TestTeamAndPlayerCreation(unittest.TestCase):
    def test_create_player(self):
        player = Player('Alice', 'shooter')
        self.assertEqual(player.name, 'Alice')
        self.assertEqual(player.position, 'shooter')

    def test_create_team(self):
        players = [
            Player('Alice', 'shooter'),
            Player('Bob', 'blocker'),
            Player('Charlie', 'marksman'),
            Player('David', 'goalie')
        ]
        team = Team('Team A', players)
        self.assertEqual(team.name, 'Team A')
        self.assertEqual(len(team.players), 4)
        self.assertEqual(team.players[0].name, 'Alice')
        self.assertEqual(team.players[1].name, 'Bob')
        self.assertEqual(team.players[2].name, 'Charlie')
        self.assertEqual(team.players[3].name, 'David')

if __name__ == '__main__':
    unittest.main()