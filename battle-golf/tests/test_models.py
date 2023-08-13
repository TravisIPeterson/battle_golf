import pytest
from unittest.mock import patch

from models import Player


def test_init():
    player = Player("Goalkeeper")
    assert player.role == "Goalkeeper"
    assert player.position == (0, 0)
    assert 1 <= player.green_number <= 8

def test_display_stats(capsys):
    player = Player("Striker", stats={"Power": 10, "Accuracy": 15})
    player.display_stats()
    captured = capsys.readouterr()
    assert "Role: Striker" in captured.out
    assert "Power: 10" in captured.out
    assert "Accuracy: 15" in captured.out

def test_select_green():
    # 1. Competitiveness dominates
    player = Player("Striker", stats={"Competitiveness": 20, "Cowardice": 10})

    results = [player.select_green() for _ in range(1000)]
    rival_green = (player.green_number + 8 // 2 - 1) % 8 + 1
    rival_count = results.count(rival_green)

    assert rival_count / 1000 > 0.2  # let's say the rival green should be selected at least 20% of the time

    # 2. Cowardice dominates
    player.stats = {"Competitiveness": 10, "Cowardice": 20}

    results = [player.select_green() for _ in range(1000)]
    left_neighbor = (player.green_number - 1) % 8 + 1
    right_neighbor = (player.green_number + 1) % 8 + 1

    neighbors_count = results.count(left_neighbor) + results.count(right_neighbor)
    assert neighbors_count / 1000 > 0.3  # let's say neighboring greens should be selected at least 30% combined

    # 3. Balanced stats
    player.stats = {"Competitiveness": 15, "Cowardice": 15}

    results = [player.select_green() for _ in range(1000)]
    count_dict = {i: results.count(i) for i in range(1, 9)}

    # Assert no green has an overly dominant selection rate
    for count in count_dict.values():
        assert 0.09 < count / 1000 < 0.15  # each green should be selected between 9% to 15% of the time


def test_drive():
    class DummyGreen:
        def __init__(self):
            self.number = 3
            self.position = (10, 10)
        
        def is_within_boundary(self, position):
            # Assume a simple boundary check for this dummy
            return -10 <= position[0] <= 10 and -10 <= position[1] <= 10

        def distance_from_center(self, position):
            return ((position[0]**2) + (position[1]**2))**0.5
    
    player = Player("Striker", stats={"Power": 15, "Accuracy": 15, "Competitiveness": 15})

    with patch('random.uniform', return_value=1.0):  # always returns maximum value
        x, y, distance = player.drive(DummyGreen(), 6)
    
    assert -10 <= x <= 10
    assert -10 <= y <= 10
    assert 0 <= distance <= 14.14  # max possible distance from center in this dummy green

# Add similar tests for block, aimed_shot, save, and run_toward_ball ...

if __name__ == "__main__":
    pytest.main()