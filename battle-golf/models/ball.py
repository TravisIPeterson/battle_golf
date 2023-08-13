import math
import time

class Ball:
    def __init__(self, x, y, radius, mass, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.acceleration_y = -9.81  # gravity, negative as it's pulling the ball downwards

    def move(self, delta_time):
        """Update position of the ball based on its velocity."""
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time

        # Apply gravity
        self.velocity_y += self.acceleration_y * delta_time

    def collide_with_ball(self, other_ball):
        """Handle collision with another ball. Elastic collision formula is applied here."""
        dx = other_ball.x - self.x
        dy = other_ball.y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < self.radius + other_ball.radius:  # Collision detected
            angle = math.atan2(dy, dx)
            sin = math.sin(angle)
            cos = math.cos(angle)

            # Rotate ball's position
            pos0 = [0, 0]
            pos1 = [dx * cos + dy * sin, dy * cos - dx * sin]

            # Rotate ball's velocity
            v0 = [self.velocity_x * cos + self.velocity_y * sin,
                  self.velocity_y * cos - self.velocity_x * sin]
            v1 = [other_ball.velocity_x * cos + other_ball.velocity_y * sin,
                  other_ball.velocity_y * cos - other_ball.velocity_x * sin]

            # Collision reaction (1D elastic collision formulas)
            v_total = v0[0] - v1[0]
            v0[0] = ((self.mass - other_ball.mass) * v0[0] + 2 * other_ball.mass * v1[0]) / (self.mass + other_ball.mass)
            v1[0] = v0[0] + v_total

            # Rotate back
            final_v0 = [v0[0] * cos - v0[1] * sin, v0[1] * cos + v0[0] * sin]
            final_v1 = [v1[0] * cos - v1[1] * sin, v1[1] * cos + v1[0] * sin]

            self.velocity_x = final_v0[0]
            self.velocity_y = final_v0[1]
            other_ball.velocity_x = final_v1[0]
            other_ball.velocity_y = final_v1[1]

            # Correct positions to prevent overlap (simple method: move to the point of contact)
            overlap = 0.5 * (distance - self.radius - other_ball.radius)
            self.x -= overlap * (self.x - other_ball.x) / distance
            self.y -= overlap * (self.y - other_ball.y) / distance
            other_ball.x += overlap * (self.x - other_ball.x) / distance
            other_ball.y += overlap * (self.y - other_ball.y) / distance

def test_ball_physics():
    # Creating two balls
    ball1 = Ball(x=0, y=10, radius=1, mass=1, velocity_x=5, velocity_y=0)
    ball2 = Ball(x=2, y=10, radius=1, mass=1, velocity_x=-5, velocity_y=0)

    delta_time = 0.01  # 10 milliseconds per time step
    total_simulation_time = 2  # Run the simulation for 1 second

    current_time = 0

    while current_time < total_simulation_time:
        ball1.move(delta_time)
        ball2.move(delta_time)

        ball1.collide_with_ball(ball2)  # Check and handle collisions

        print(f"Time: {current_time:.2f}")
        print(f"Ball1 - x: {ball1.x:.2f}, y: {ball1.y:.2f}, velocity_x: {ball1.velocity_x:.2f}, velocity_y: {ball1.velocity_y:.2f}")
        print(f"Ball2 - x: {ball2.x:.2f}, y: {ball2.y:.2f}, velocity_x: {ball2.velocity_x:.2f}, velocity_y: {ball2.velocity_y:.2f}")
        print("-----------")

        current_time += delta_time
        time.sleep(delta_time)  # Optional: To see the printed results at a more readable pace

if __name__ == "__main__":
    test_ball_physics()
