import math

class interval:
    def __init__(self, _min=float('inf'), _max=float('-inf')):
        self.min = _min
        self.max = _max

    def size(self):
        return self.max - self.min

    def contains(self, x):
        return self.min <= x <= self.max

    def surrounds(self, x):
        return self.min < x < self.max

    def clamp(self, x):
        if x < self.min: return self.min
        if x > self.max: return self.max
        return x

    def expand(self, delta):
        padding = delta / 2
        return interval(self.min - padding, self.max + padding)

# Constants for convenience
interval_empty = interval(float('inf'), float('-inf'))
interval_universe = interval(float('-inf'), float('inf'))