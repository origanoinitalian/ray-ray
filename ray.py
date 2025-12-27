from vec3 import vec3, point3, color, unit_vector

class Ray:
    def __init__(self, origin, direction):
        self.orig = origin
        self.direction_vec = direction

    def at(self, t):
        return self.orig + (self.direction_vec * t)

def ray_color(r):
    # Use the unit_vector function you defined in vec3.py
    unit_direction = unit_vector(r.direction_vec)
    
    # Use .y WITHOUT () because of your @property
    a = 0.5 * (unit_direction.y + 1.0)
    
    # This is the "Lerp" (White to Blue)
    return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0)