import math
from vec3 import dot
from hittable import hit_record

class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    @staticmethod
    def get_sphere_uv(p):
        theta = math.acos(-p.y)
        phi = math.atan2(-p.z, p.x) + math.pi
        u = phi / (2 * math.pi)
        v = theta / math.pi
        return u, v

    def hit(self, r, ray_t, rec):
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
        if not ray_t.surrounds(root):
            root = (-h + sqrtd) / a
            if not ray_t.surrounds(root):
                return False

        rec.t = root # Distance along ray
        rec.p = r.at(rec.t)  # coordinates of Point of intersection
        rec.material = self.material
        outward_normal = (rec.p - self.center) / self.radius # Normal vector at intersection
        rec.set_face_normal(r, outward_normal)
        rec.u, rec.v = Sphere.get_sphere_uv(outward_normal) # Texture cmapping 3D to 2D
        return True