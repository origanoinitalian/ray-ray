from hittable import hittable, hit_record
from vec3 import vec3, dot, cross, unit_vector
from ray import Ray
from interval import interval

class Quad(hittable):
    def __init__(self, Q, u, v, mat):
        self.Q = Q   # Starting corner
        self.u = u   # Vector for side 1
        self.v = v   # Vector for side 2
        self.mat = mat
        
        # Calculate the plane parameters
        n = cross(u, v)
        self.normal = unit_vector(n)
        self.D = dot(self.normal, Q) # The 'D' in Ax + By + Cz = D
        self.w = n / dot(n, n)       # Constant for interior testing
        
    def hit(self, r, ray_t, rec):
        denom = dot(self.normal, r.direction_vec)

        # No hit if the ray is parallel to the plane
        if abs(denom) < 1e-8:
            return False

        # Solve for t (intersection point on the infinite plane)
        t = (self.D - dot(self.normal, r.orig)) / denom
        if not ray_t.contains(t):
            return False

        # Determine if the hit point is inside the quad boundaries
        intersection = r.at(t)
        planar_hitpt_vector = intersection - self.Q
        
        # Calculate alpha and beta (u,v coordinates on the quad surface)
        alpha = dot(self.w, cross(planar_hitpt_vector, self.v))
        beta = dot(self.w, cross(self.u, planar_hitpt_vector))

        if not self.is_interior(alpha, beta, rec):
            return False

        # Ray hits the quad; fill the record
        rec.t = t
        rec.p = intersection
        rec.material = self.mat
        rec.set_face_normal(r, self.normal)
        return True

    def is_interior(self, a, b, rec):
        # Check if alpha and beta are between 0 and 1
        if (a < 0) or (1 < a) or (b < 0) or (1 < b):
            return False
        
        rec.u = a
        rec.v = b
        return True