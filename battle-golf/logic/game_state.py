from collections import deque

import unittest

class GameState:

    AIMED_SHOT = "aimed_shot"
    ATTEMPT_LEAP = "attempt_leap"
    BLOCK = "block"
    DRIVE = "drive"
    FALL_INTO_HOLE = "fall_into_hole"
    IDLE = "idle"
    NEOLIBERAL_AGENDA = "neoliberal_agenda"
    SAVE = "save"

    transitions = {
        AIMED_SHOT: [ATTEMPT_LEAP, BLOCK, SAVE],
        ATTEMPT_LEAP: [FALL_INTO_HOLE, SAVE],
        DRIVE: [BLOCK, NEOLIBERAL_AGENDA, SAVE],
        FALL_INTO_HOLE: [AIMED_SHOT, DRIVE, NEOLIBERAL_AGENDA],
        IDLE: [AIMED_SHOT, ATTEMPT_LEAP, BLOCK, DRIVE, FALL_INTO_HOLE, NEOLIBERAL_AGENDA, SAVE],
        NEOLIBERAL_AGENDA: [AIMED_SHOT, ATTEMPT_LEAP, BLOCK, DRIVE, FALL_INTO_HOLE, NEOLIBERAL_AGENDA, SAVE],
        SAVE: [AIMED_SHOT, DRIVE, FALL_INTO_HOLE, NEOLIBERAL_AGENDA]
    }

    def __init__(self):
        self.current_state = "idle"
        self.history = deque([self.current_state], maxlen=2)
    
    def can_transition(self, new_state):
        return new_state in self.available_actions()
    
    def perform_transition(self, new_state):
        if self.can_transition(new_state):
            self.history.append(new_state)
            self.current_state = new_state
            return True
        return False
    
    def available_actions(self):
        if list(self.history) == [self.ATTEMPT_LEAP, self.SAVE]:
            return [self.FALL_INTO_HOLE]
        return self.transitions.get(self.current_state, [])
    
class TestGameState(unittest.TestCase):

    def setUp(self):
        self.game_state = GameState()

    def test_initial_state(self):
        # Ensure the game starts in the "idle" state
        self.assertEqual(self.game_state.current_state, GameState.IDLE)

    def test_transitions(self):
        # Test the basic transitions
        self.assertTrue(self.game_state.perform_transition(GameState.AIMED_SHOT))
        self.assertEqual(self.game_state.current_state, GameState.AIMED_SHOT)

        self.assertTrue(self.game_state.perform_transition(GameState.BLOCK))
        self.assertEqual(self.game_state.current_state, GameState.BLOCK)

    def test_invalid_transition(self):
        # Test invalid transitions
        self.game_state.perform_transition(GameState.AIMED_SHOT)
        self.assertFalse(self.game_state.perform_transition(GameState.DRIVE))  # DRIVE is not a valid next action after AIMED_SHOT

    def test_special_sequence(self):
        # Test the sequence [ATTEMPT_LEAP, SAVE]
        self.assertTrue(self.game_state.perform_transition(GameState.ATTEMPT_LEAP))
        self.assertTrue(self.game_state.perform_transition(GameState.SAVE))
        self.assertEqual(self.game_state.available_actions(), [GameState.FALL_INTO_HOLE])

    def test_history_limit(self):
        # Ensure the history deque maintains only the last two states
        self.game_state.perform_transition(GameState.AIMED_SHOT)
        self.assertEqual(list(self.game_state.history), [GameState.IDLE, GameState.AIMED_SHOT])

        self.game_state.perform_transition(GameState.BLOCK)
        self.assertEqual(list(self.game_state.history), [GameState.AIMED_SHOT, GameState.BLOCK])

if __name__ == '__main__':
    unittest.main()