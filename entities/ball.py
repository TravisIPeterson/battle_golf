class Ball:
    def __init__(self, position, initial_velocity, angle, mass, radius, physics_engine):
        self.position = position
        self.velocity = initial_velocity
        self.angle = angle
        self.mass = mass
        self.radius = radius
        self.physics_engine = physics_engine
        self.on_green = None
        self.green_owner = None
        self.in_possession = False
        self.possession_owner = None
        self.on_ground = False

    def update(self, time):
        # Update the position and velocity of the ball based on the calculated trajectory
        trajectory = self.physics_engine.calculate_trajectory(self.velocity, self.angle, time)
        self.position += trajectory.x, trajectory.y
        self.velocity = trajectory.total_v_x, trajectory.total_v_y

        # Check if the ball is on a green
        if self.position[1] <= 0:
            self.on_green = True
        else:
            self.on_green = False

        # Check if the ball is in possession of a player
        if self.in_possession:
            self.on_ground = True
        else:
            self.on_ground= False

    def set_possession(self, player):
        # Set the possession owner of the ball
        self.in_possession = True
        self.possession_owner = player

    def clear_possession(self):
        # Clear the possession owner of the ball
        self.in_possession = False
        self.possession_owner = None

    def set_on_green(self, team):
        # Set the green owner of the ball
        self.on_green = team

    def off_green(self, team):
        # Clear the green owner of the ball
        self.on_green = None