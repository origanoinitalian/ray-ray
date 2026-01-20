from vec3 import random_in_unit_sphere, random_unit_vector, vec3, point3, color, unit_vector, dot
from hittable import hit_record
from interval import interval

class Ray:
    def __init__(self, origin, direction):
        self.orig = origin
        self.direction_vec = direction

    def at(self, t):
        return self.orig + (self.direction_vec * t) # P(t) = A + t*b
    

def ray_color(r, world, depth):
    if depth <= 0:
        return color(0,0,0) # Stop if we've bounced too many times

    rec = hit_record()

    if not world.hit(r, interval(0.001, float('inf')), rec):
        return color(0, 0, 0)
    
    # Get light emitted by the material
    color_from_emission = rec.material.emitted(rec.u, rec.v, rec.p)

    # Check if the material scatters light (like Metal or Lambertian)
    was_scattered, scattered_ray, attenuation = rec.material.scatter(r, rec)

    # Ask the material to scatter the ray
    
    if was_scattered:
        # Standard recursive bounce
        return color_from_emission + attenuation * ray_color(scattered_ray, world, depth - 1)
    else:
        return color_from_emission
    # if no hits, return sky gradient
    unit_direction = unit_vector(r.direction_vec)
    
    a = 0.5 * (unit_direction.y + 1.0)
    
    # The "Lerp" (White to Blue)
    return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(1.0, 0.7, 0.8)