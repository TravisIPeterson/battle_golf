class Ball:
    def __init__(self, current_green=None, all_greens=[]):
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.current_green = current_green
        self.all_greens = all_greens

    def move(self):
        if self.current_green:
            slope = self.current_green.calculate_slope(self.position)
            force_due_to_slope = slope * 0.01
            
            x, y = self.position
            distance_to_center = (x ** 2 + y ** 2) ** 0.5
            if distance_to_center > 0:
                dx_center = -x / distance_to_center * force_due_to_slope
                dy_center = -y / distance_to_center * force_due_to_slope
                self.velocity = (self.velocity[0] + dx_center, self.velocity[1] + dy_center)

        new_x = self.position[0] + self.velocity[0]
        new_y = self.position[1] + self.velocity[1]
        self.position = (new_x, new_y)

        if self.current_green and not self.current_green.is_within_boundary(self.position):
            self.current_green = None

        self.check_for_new_green()

    def check_for_new_green(self):
        for green in self.all_greens:
            if green.is_within_boundary(self.position):
                self.current_green = green
                break