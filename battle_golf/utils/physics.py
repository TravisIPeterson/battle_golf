import math
from entities.wind import Wind

class PhysicsEngine:
    def __init__(self, wind=Wind()):
        self.wind = wind

    def calculate_trajectory(self, initial_velocity, angle, time, on_ground, ground_angle):
        # Calculate the trajectory of the ball based on its initial velocity and angle
        # and the effects of wind and physical objects

        # Calculate the x and y components of the initial velocity
        v_x = initial_velocity * math.cos(angle)
        v_y = initial_velocity * math.sin(angle)

        # Calculate the x and y components of the wind velocity
        wind_speed = self.wind.get_speed()
        wind_direction = self.wind.get_direction()
        w_x = wind_speed * math.cos(wind_direction)
        w_y = wind_speed * math.sin(wind_direction)

        # Calculate the x and y components of the total velocity
        total_v_x = v_x + w_x
        total_v_y = v_y + w_y

        # Calculate the x and y components of the acceleration due to gravity
        g_x = 0
        g_y = -9.81

        # Calculate the x and y components of the displacement
        if on_ground:
            x = initial_velocity * math.cos(ground_angle) * time
            y = initial_velocity * math.sin(ground_angle) * time
        else:
            x = initial_velocity * math.cos(angle) * time
            y = initial_velocity * math.sin(angle) * time + 0.5 * g_y * time ** 2

        # Calculate the angle of the ground at the current position
        if on_ground:
            ground_angle = math.atan2(-g_y, g_x)

        # Calculate the effect of wind on the ball's trajectory
        if not on_ground:
            wind_effect = (1 + time) ** 2
            total_v_x += w_x * wind_effect
            total_v_y += w_y * wind_effect

        return total_v_x, total_v_y, x, y, ground_angle

    def apply_wind(self, velocity, time):
        # Apply the effect of wind on the ball's velocity
        wind_speed = self.wind.get_speed()
        wind_direction = self.wind.get_direction()
        w_x = wind_speed * math.cos(wind_direction)
        w_y = wind_speed * math.sin(wind_direction)
        wind_effect = (1 + time) ** 2
        return velocity + w_x * wind_effect, velocity + w_y * wind_effect

    def apply_obstacle(self, velocity, obstacle):
        # Apply the effect of an obstacle on the ball's velocity
        return velocity - obstacle.friction_coefficient * velocity

    def apply_bounce(self, velocity, ground_angle):
        # Apply the effect of a bounce on the ball's velocity
        return -velocity * math.sin(ground_angle)

    def apply_roll(self, position, ground_angle):
        # Apply the effect of rolling on the ball's position
        return position + math.tan(ground_angle) * position