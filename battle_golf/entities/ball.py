class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.in_possession = False
        self.on_green = False
        self.green = None

    def set_possession(self, team):
        self.in_possession = True
        self.possession_team = team

    def clear_possession(self):
        self.in_possession = False
        self.possession_team = None

    def set_on_green(self, green):
        self.on_green = True
        self.green = green

    def clear_on_green(self):
        self.on_green = False
        self.green = None

    def move(self, dx, dy):
        self.x += dx
        self.y += dy