from vec3 import random_in_unit_sphere, random_unit_vector, vec3, point3, color, unit_vector, dot
from hittable import hit_record
from interval import interval

class Ray:
    def __init__(self, origin, direction):
        self.orig = origin
        self.direction_vec = direction

    def at(self, t):
        return self.orig + (self.direction_vec * t) # P(t) = O + t*d
    

def ray_color(r, world, depth): # the eye with rules of interval
    if depth <= 0:
        return color(0,0,0) # Stop ray from bouncing forever

    rec = hit_record()

    if not world.hit(r, interval(0.001, float('inf')), rec): # check the ray hit an object  
        return color(0, 0, 0)
    
    color_from_emission = rec.material.emitted(rec.u, rec.v, rec.p)

    was_scattered, scattered_ray, attenuation = rec.material.scatter(r, rec)
    
    if was_scattered:
        return color_from_emission + attenuation * ray_color(scattered_ray, world, depth - 1)
    else:
        return color_from_emission
    # if no hits, return sky gradient
    unit_direction = unit_vector(r.direction_vec)
    
    a = 0.5 * (unit_direction.y + 1.0)
    
    # The "Lerp" (White to Blue)
    return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(1.0, 0.7, 0.8)