import math
from vec3 import dot
from hittable import hit_record

class Sphere:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def hit(self, r, t_min, t_max, rec):
        oc = r.orig - self.center
        a = r.direction_vec.length_squared()
        h = dot(r.direction_vec, oc)
        c = oc.length_squared() - self.radius**2
        discriminant = h*h - a*c

        if discriminant < 0:
            return False
        
        sqrtd = math.sqrt(discriminant)
        # Find the nearest root in the acceptable range
        root = (-h - sqrtd) / a
        if root <= t_min or t_max <= root:
            root = (-h + sqrtd) / a
            if root <= t_min or t_max <= root:
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        return True