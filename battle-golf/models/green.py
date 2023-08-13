class Green:
    def __init__(self, radius=50, max_slope=15, friction_factor=0.1):
        self.radius = radius
        self.max_slope = max_slope
        self.friction_factor = friction_factor
        self.ball_position = None  # This could be a tuple (x, y)

    def calculate_slope(self, position):
        distance_from_center = self.distance_from_center(position)
        slope = (distance_from_center / self.radius) * self.max_slope
        return slope

    def distance_from_center(self, position):
        # Assuming the center is (0,0)
        x, y = position
        return ((x**2) + (y**2))**0.5

    def move_ball(self, initial_speed):
        if self.ball_position == (0, 0):  # If ball is at the center
            return

        slope = self.calculate_slope(self.ball_position)
        speed = initial_speed - (slope * self.friction_factor)

        if speed <= 0:  # If the ball doesn't have enough speed to move
            return

        # Adjust the position based on the speed and the direction
        # For simplicity, assuming it always moves towards the center (0, 0)
        # You might use some vector math to handle different directions

        x, y = self.ball_position
        direction_to_center_x = -x / self.radius
        direction_to_center_y = -y / self.radius

        new_x = x + direction_to_center_x * speed
        new_y = y + direction_to_center_y * speed

        self.ball_position = (new_x, new_y)
    
    def is_within_boundary(self, position):
        # Check if a position is within the green's boundary
        distance = self.distance_from_center(position)
        return distance <= self.radius