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