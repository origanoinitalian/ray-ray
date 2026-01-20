from vec3 import dot
from interval import interval

class hittable:     #abstraction to say quad is hittable
    def hit(self, r, ray_t, rec):
        return False

class hit_record:
    def __init__(self):
        self.p = None       # Point of intersection
        self.normal = None  # Normal vector at intersection
        self.t = 0          # Distance along ray
        self.u = 0          # Texture coordinate u
        self.v = 0          # Texture coordinate v
        self.front_face = False
        self.material = None  

    def set_face_normal(self, r, outward_normal):
        # Decide if the ray is hitting the inside or outside
        self.front_face = dot(r.direction_vec, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

class hittable_list:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def hit(self, r, ray_t, rec):
        temp_rec = hit_record()
        hit_anything = False
        closest_so_far = ray_t.max

        for obj in self.objects:
            if obj.hit(r, interval(ray_t.min, closest_so_far), temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                # Copy the temp_rec values to our main record
                rec.t = temp_rec.t
                rec.p = temp_rec.p
                rec.u = temp_rec.u
                rec.v = temp_rec.v
                rec.normal = temp_rec.normal
                rec.front_face = temp_rec.front_face
                rec.material = temp_rec.material
        
        return hit_anything