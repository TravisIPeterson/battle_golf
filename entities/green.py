class Green:
    def __init__(self, team, x, y, radius, hole_x, hole_y):
        self.team = team
        self.x = x
        self.y = y
        self.radius = radius
        self.hole_x = hole_x
        self.hole_y = hole_y

    def contains(self, x, y):
        # Check if the point (x, y) is within the green
        return (x - self.x)**2 + (y - self.y)**2 <= self.radius**2