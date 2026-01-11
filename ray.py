from vec3 import random_in_unit_sphere, random_unit_vector, vec3, point3, color, unit_vector, dot
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

def ray_color(r, world, depth):
    if depth <= 0:
        return color(0,0,0) # Stop if we've bounced too many times

    rec = hit_record()

    if world.hit(r, 0.001, float('inf'), rec):

        # Ask the material to scatter the ray
        was_scattered, scattered_ray, attenuation = rec.material.scatter(r, rec)
        if was_scattered:
            # The color is (Material Color) * (Light from the next bounce)
            return attenuation * ray_color(scattered_ray, world, depth - 1)
        return color(0, 0, 0)
    
    # if no hits, return sky gradient
    unit_direction = unit_vector(r.direction_vec)
    
    a = 0.5 * (unit_direction.y + 1.0)
    
    # This is the "Lerp" (White to Blue)
    return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0)