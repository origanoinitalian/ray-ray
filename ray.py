from vec3 import vec3, point3, color, unit_vector, dot
from hittable import hit_record

class Ray:
    def __init__(self, origin, direction):
        self.orig = origin
        self.direction_vec = direction

    def at(self, t):
        return self.orig + (self.direction_vec * t)
    

def hit_sphere(center, radius, r):
    oc = r.orig - center
    a = dot(r.direction_vec, r.direction_vec)
    b = 2.0 * dot(oc, r.direction_vec)
    c = dot(oc, oc) - radius*radius
    discriminant = b*b - 4*a*c
    return (discriminant > 0)

def ray_color(r, world):

    rec = hit_record()

    if world.hit(r, 0.001, float('inf'), rec):
        # Simple normal-based coloring
        return 0.5 *(rec.normal +color(1, 0, 0)) 
    
    # if no hits, return sky gradient
    unit_direction = unit_vector(r.direction_vec)
    
    a = 0.5 * (unit_direction.y + 1.0)
    
    # This is the "Lerp" (White to Blue)
    return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0)