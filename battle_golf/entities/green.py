class Green:
    def __init__(self, team, x, y, radius, hole_x, hole_y):
        self.team = team
        self.x = x
        self.y = y
        self.radius = radius
        self.hole_x = hole_x
        self.hole_y = hole_y

greens = [
    Green(team='Team A', x=0, y=0, radius=10, hole_x=0, hole_y=0),
    Green(team='Team B', x=20, y=0, radius=10, hole_x=20, hole_y=0),
    Green(team='Team C', x=10, y=17.32, radius=10, hole_x=10, hole_y=17.32),
    Green(team='Team D', x=-10, y=17.32, radius=10, hole_x=-10, hole_y=17.32),
    Green(team='Team E', x=-20, y=0, radius=10, hole_x=-20, hole_y=0),
    Green(team='Team F', x=-10, y=-17.32, radius=10, hole_x=-10, hole_y=-17.32),
    Green(team='Team G', x=10, y=-17.32, radius=10, hole_x=10, hole_y=-17.32),
    Green(team='Team H', x=0, y=0, radius=10, hole_x=0, hole_y=0)
] 