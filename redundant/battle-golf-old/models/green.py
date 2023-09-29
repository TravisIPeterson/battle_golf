class Green:
    def __init__(self, number):
        self.number = number
        self.ball_on_green = False  # True if ball is currently on this green.

    def place_ball_on_green(self):
        # Method to indicate that the ball has been placed on this green.
        self.ball_on_green = True

    def remove_ball_from_green(self):
        # Method to indicate that the ball has been removed from this green.
        self.ball_on_green = False

    def is_ball_on_green(self):
        # Method to check if the ball is currently on this green.
        return self.ball_on_green